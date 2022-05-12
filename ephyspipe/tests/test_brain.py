import ephyspipe.brain as brain
import ephyspipe.behavior as bhv
import numpy as np
from ephyspipe.config import TESTDATADIR
from os.path import join as pjoin


def test_get_fr():
    # ignore edge effects for smoothing window = 49
    ntimes = 200
    edge = 24
    valid_idx = np.arange(edge, ntimes - edge)

    # make fake input raster
    fake_raster = np.concatenate([np.zeros((1, ntimes)), \
                                  np.ones((1, ntimes)), \
                                  np.zeros((1, ntimes))], axis=0)
    fake_raster[2, int(ntimes/2)] = 1

    # make fake firing rates
    fake_fr = np.concatenate([np.zeros((1, ntimes)), \
                              np.ones((1, ntimes)), \
                              np.zeros((1, ntimes))], axis=0)
    fake_fr[2, int(ntimes / 2 - edge):int(ntimes / 2 + edge + 1)] = 0.02

    # get smoothed firing rates
    output = brain.get_fr(fake_raster).round(2)

    # compare!
    assert np.all(output[:, valid_idx] == fake_fr[:, valid_idx])


def test_get_raster():
    # make some fake data
    fake_data = dict({"neuron_A" : [0, 1, 2, 3, 4, 5], \
                 "neuron_B" : [10]})
    unit_names = [key for key in fake_data.keys()]
    ntimes = 20

    # make fake rasters
    fake_raster = np.zeros((len(unit_names), ntimes))
    fake_raster[0, fake_data["neuron_A"]] = 1
    fake_raster[1, fake_data["neuron_B"]] = 1

    # get rasters
    output = brain.get_raster(fake_data, unit_names, ntimes)

    # compare!
    assert np.all(output == fake_raster)


def test_chop():
    # make fake brain data
    nunits = 5
    ntimes = 250
    fake_data = np.arange(ntimes).reshape((nunits, -1))
    sync_points = np.array([0.010, 0.020])
    window = (-0.003, 0.003)
    ntimes_chopped = np.arange(window[0], window[1], .001).shape[0]

    # simulated chopped up data
    slice = np.array([range(7, 13), range(17, 23)])
    slice_offset = np.tile(np.arange(0, ntimes, \
                                     ntimes / nunits).reshape((1, 1, nunits)),
                           (sync_points.shape[0], ntimes_chopped, 1))
    fake_chopped = np.repeat(slice[:, :, np.newaxis], nunits, axis=2) + \
                   slice_offset

    # get chopped data
    output = brain.chop(fake_data, sync_points, window)

    # compare!
    assert np.all(output == fake_chopped)


def test_sliding_avg():
    # make fake data
    nsync = 5
    fake_row = np.repeat(np.arange(10), 10).reshape((1, -1))
    fake_data = np.tile(fake_row, [nsync, 1]).reshape((nsync, -1, 1))
    ts = np.arange(0, fake_data.shape[1]/1000, 0.001)
    t_range = (ts[0], ts[-1])
    window = 0.010

    # make fake output
    fake_smooth = np.tile(np.arange(9).reshape((1, -1)), [nsync, 1])
    _, data_smooth = brain.sliding_avg(fake_data, ts, t_range, window, step=1)

    # compare!
    assert np.all(data_smooth[:, :, 0] == fake_smooth)


def test_raw_spk():
    # use saved mini sample data
    sample_spk = pjoin(TESTDATADIR, "sample_spk.mat")
    nunits = 2
    ntimes = 82670

    # expected unit names
    unit_names = ["SPK_SPKC001a", "SPK_SPKC001b"]

    # expected raster
    sample_raster = np.zeros((nunits, ntimes))
    sample_raster[0,[20000, 25000, 30000, 35000]] = 1
    sample_raster[1, [80010, 81670]] = 1

    # expected firing rates
    sample_fr = brain.get_fr(sample_raster)

    # process sample data
    output = brain.process_raw_spk(sample_spk, channels=-1)

    # compare!
    assert np.all(output[0] == sample_raster)
    assert np.all(output[1] == sample_fr)
    assert np.all(output[2].ID == unit_names)


def test_raw_lfp():
    # use saved mini sample lfp
    sample_lfp = pjoin(TESTDATADIR, "sample_lfp.mat")
    sync_points = np.array([3, 6, 9])
    time_range = (-0.01, 0.01)

    # expected outputs
    channel_names = ["FP001", "FP002"]
    ntimes = np.arange(-0.01, 0.01, 0.001).shape[0]
    expected_magmeans = np.array([-0.2, 0.1])

    # process LFP sample
    output = brain.process_raw_lfp(sample_lfp, sync_points, time_range)

    # compare!
    output_magmeans = output[0][1].mean(axis=0).mean(axis=0).round(1)
    assert np.all(output_magmeans == expected_magmeans)
    assert output[2].shape[0] == ntimes
    assert np.all(output[3].ID == channel_names)
