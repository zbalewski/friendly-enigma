import ephyspipe.behavior as bhv
from ephyspipe.config import TESTDATADIR
from os.path import join as pjoin
import numpy as np

def test_raw_bhv():
    # load mini bhv sample
    sample_bhv = [pjoin(TESTDATADIR, "sample_bhv.mat")]

    # expecting 3 trial
    sample_Trial = [np.array(i + 1) for i in range(3)] # trial num 1-3
    sample_TrialError = [np.array(0) for i in range(3)] # error code, all 0s

    # load raw bhv
    output = bhv.load_raw_bhv(sample_bhv)

    # compare!
    assert np.all(output["Trial"] == sample_Trial)
    assert np.all(output["TrialError"] == sample_TrialError)


def test_pl2_codes():
    # use mini spk sample
    sample_spk = pjoin(TESTDATADIR, "sample_spk.mat")

    # expecting 3 trials, with start and stop codes
    ntrials = 3
    start_code = 9
    stop_code = 18

    # load codes
    output = bhv.load_pl2_codes(sample_spk)
    output_starts = np.where(output["event_codes"] == start_code)[0].shape[0]
    output_stops = np.where(output["event_codes"] == stop_code)[0].shape[0]

    # compare!
    assert output_starts == ntrials
    assert output_stops == ntrials


def test_events():
    # load mini bhv sample
    sample_bhv = [pjoin(TESTDATADIR, "sample_bhv.mat")]
    sample_bhv_data = bhv.load_raw_bhv(sample_bhv)

    # load mini spk sample
    sample_spk = pjoin(TESTDATADIR, "sample_spk.mat")
    sample_pl2_codes = bhv.load_pl2_codes(sample_spk)

    # get time of trial output_starts
    event = 9

    # expected times:
    sample_trialstarts = np.array([12.7, 134.7, 139.2])

    # extract sync_points
    output = bhv.get_trial_events(sample_bhv_data, sample_pl2_codes, event)

    # compare!
    assert np.all(output.round(1) == sample_trialstarts)
