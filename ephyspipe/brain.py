import mat73
import h5py

import numpy as np
import pandas as pd

import scipy.signal as signal
import scipy.stats as stats

def process_raw_spk(spk_fname, channels=-1):
    """
    Load raw spk (.pl2 saved as .mat)

    Parameters:
    ----------
    spk_fname : string
        Path file for raw spk data
    channels : list
        Integers, restrict processing to these channel numbers; if -1, use all channels

    Returns:
    -------
    raster : np array
        spike trains, nunits x ntimes
    fr : np array
        firing rates, nunits x ntimes
    unit_meta : pd table
        meta data; each row corresponds to row in raster and fr

    """

    # load spk data
    data = mat73.loadmat(spk_fname)

    # get unique unit names
    unit_names = [u[0] for u in data["unit_names"]]
    if channels!=-1:
        unit_names = [u for u in unit_names if int(u[8:11]) in channels]
    nunits = len(unit_names)

    # get last spike time in entire session, +1 second
    last_spk = [data[u][-1] for u in unit_names]
    max_t = 1 + max(last_spk)
    ts = np.arange(np.round(1000 * max_t)) # ms, corresponding time vector
    ntimes = len(ts)

    # get spike trains for all units
    raster = get_raster(data, unit_names, ntimes)

    # smooth spike trains into firig rates
    fr = get_fr(raster)

    # save some meta data for each unit
    mean_fr = [len(data[u])/max_t for u in unit_names]
    channel = [int(u.replace("SPK_SPKC","")[:3]) for u in unit_names]
    unit_meta = pd.DataFrame({"ID" : unit_names,
                              "channel" : channel,
                              "mean_fr" : mean_fr})

    return raster, fr, unit_meta


def get_raster(data, unit_names, ntimes):
    """
    Turn spike times into trains, for all units in data.

    Parameters:
    ----------
    data : dict
        spk data, with unit spike times plus some meta data
    unit_names : list of strings
        unit names
    ntimes : int
        index of max time point

    Returns:
    -------
    raster : 2D np array
        units x time, spikes @ 1 kHz

    """
    nunits = len(unit_names)
    raster = np.empty((nunits, ntimes))
    for u in range(nunits):
        raster[u, :] = ts_to_train(data[unit_names[u]], ntimes)

    return raster


def get_fr(raster):
    """
    Turn raster (for units x entire session) into firing rates.

    Parameters:
    ----------
    raster : 2D np array
        units x time, spikes @ 1 kHz

    Returns:
    -------
    fr : 2D np array
        units x time, firing rates @ 1kHz (per ms; *1000 to get Hz)

    """
    fr = np.empty(raster.shape)
    for u in range(raster.shape[0]):
        fr[u, :] = train_to_fr(raster[u, :])

    return fr


def ts_to_train(timestamps, ntimes):
    """
    Turn spike timestamps into a spike train.

    Parameters:
    ----------
    timestamps : np vector
        Times this unit fired, in sec
    ntimes : int
        Max time index

    Returns:
    -------
    train : np vector
        1 or 0 to indicate spike in that time window

    """

    # make train of same size
    train = np.zeros((1, ntimes))

    # set train = 1 at closest time stamp
    timestamps_ms = np.round(1000 * timestamps).astype(int)
    train[:, timestamps_ms] = 1

    return train


def train_to_fr(train):
    """
    Turn spike train into firing rate.
    Note: can also use this to smooth LFP magnitude!

    Parameters:
    ----------
    train : np vector
        1 or 0 to indicate spike in that time window

    Returns:
    -------
    train_smoothed : np vector
        train with 50 ms boxcar smoothing

    """
    # define boxcar smooth
    box = signal.boxcar(49) / 49

    # apply smoothing
    train_smoothed = np.convolve(train, box, "same")

    return train_smoothed


def chop(long_brain, sync_points, window):
    """
    Chop up 2 hr session into snippets around sync points.

    Parameters:
    ----------
    long_brain : 2D np array
        units x time (e.g. spike train, LFP magnitude)
    sync_points : np vector
        sync points across session, e.g. start time for all trials
    window : tuple (2 element)
        time window around sync point (in seconds)

    Returns:
    -------
    chopped_brain : 3D np array
        sync_points x time x units

    """
    # number of units
    nunits = long_brain.shape[0]

    # time window index
    t_idx = np.arange(window[0] * 1000, window[1] * 1000) # use ms!
    nt = t_idx.shape[0]

    # sync point index
    sync_idx = np.round(sync_points * 1000) # use ms!
    sync_idx[sync_idx == -1000] = -1 # manual fix; these trials are missing events
    nsync = sync_idx.shape[0]

    # make index matrix
    tile_time = np.tile(t_idx.reshape(1, -1), (nsync, 1))
    tile_sync = np.tile(sync_idx.reshape(-1, 1), (1, nt))

    long_idx = (tile_time + tile_sync).astype(int)
    long_idx[tile_sync == -1] = -1 # same manual fix

    # chop up each unit...
    chopped_brain = np.empty((nsync, nt, nunits))
    for u in range(nunits):
        chopped_brain[:, :, u] = long_brain[u, :][long_idx]

    if nunits == 1:
        chopped_brain = np.squeeze(chopped_brain)

    return chopped_brain



def sliding_avg(data, ts, time_range, window, step=0.25):
    """
    Downsample by averaging in window offset by step (window fraction)
    along axis=1 (time). Assume data @ 1 kHz, and window given in
    seconds; step is fraction of window.

    TODO: make this more flexible for other time units; will still run right
    now but results could be incorrect...

    Parameters:
    ----------
    data : 3D np array
        sync points x time x sources, sampled at 1 kHz; sources are units or channels
    ts : np vector
        timestamps corresponding to time axis in data, assume seconds
    time_range : tuple
        restricted time range from full ts
    window : float
        size of averging window
    step : float
        offset between averaging windows, given by fraction of
        window; must be >0, and 1 = no overlap.

    Returns:
    -------
    mid_times : np vector
        time stamps for smoothed data
    data_smooth : 2D np array
        smoothed data: sync_points x time x sources
    """

    # check that step makes sense...
    if step <= 0 or step > 1:
        raise ValueError("Bad choice for sliding window average! " +\
                         "step' is fraction of window, must be > 0 and <= 1")

    # check that time range makes sense...
    if time_range[0] >= time_range[1]:
        raise ValueError("Bad choice for sliding window average! " +\
                        "'time_range' is not sensible")
    adjusted_time_range = np.array([
        np.max([time_range[0], ts[0]]),
        np.min([time_range[1], ts[-1]])])

    # get size of data
    nsync, ntimes, nsources = data.shape

    # set window and offset sizes, in ms
    window_ms = np.round(1000 * window)
    offset_ms = np.round(window_ms * step)

    # find midpoints for averaging windows
    start_idx = np.floor(np.argmin(np.abs(ts - adjusted_time_range[0])) + window_ms/2)
    stop_idx = np.ceil(1 + np.argmin(np.abs(ts - adjusted_time_range[1])) - window_ms/2)
    mid_idx = np.arange(start_idx, stop_idx, offset_ms).astype(int)
    mid_times = ts[mid_idx]

    # do sliding averages
    data_smooth = np.empty((nsync, len(mid_idx), nsources))
    t_idx = np.arange(-np.floor(window_ms / 2), np.ceil(window_ms / 2)).astype(int)

    for i in range(len(mid_idx)):
        data_smooth[:, i, :] = data[:, mid_idx[i] + t_idx, :].mean(axis=1)


    return mid_times, data_smooth


def process_raw_lfp(lfp_fname, sync_point, time_range, channels=-1):
    """
    Load raw lfp (.pl2 saved as .mat)

    Parameters:
    ----------
    lfp_fname : string
        Path file for raw lfp data
    sync_point : np vector
        Times to sync across session (e.g. trial start)
    time_range : 2 element tuple
        Time range around sync points, in sec
    channels : list
        Integers; restrict to these channels; -1 = all

    Returns:
    -------
    band_mag_chopped_np : list
        of 3D np arrays with each bandpass magnitude; sync_points x time x channels
    band_phs_chopped_np : list
        of 3D np arrays with each bandpass phase; sync_points x time x channels
    ts_chopped : np vector
        time for data chopped at sync_points, in sec
    lfp_meta : pd table
        meta data; each row corresponds to LFP channel

    """

    # get channel names
    f = h5py.File(lfp_fname, "r")
    channel_names = [key for key in f.keys() if key.find("FP") == 0]
    if channels!=-1:
        channel_names = [ch for ch in channel_names if int(ch[2:]) in channels]

    # get lfp time
    data = mat73.loadmat(lfp_fname, only_include="lfp_ts")
    ts_long = data["lfp_ts"]/1000 # time in seconds

    # make notch filters
    notch_hz = [60, 120, 180] # Hz
    notch_filts = [signal.iirnotch(n, n, 1000) for n in notch_hz]

    # make bandpass filters
    band_hz = [[2, 4], [4, 8], [8, 12], [12, 30], [30, 60], [70, 200]] # Hz
    band_names = ["delta", "theta", "alpha", "beta", "gamma", "high gamma"]
    band_filts = [signal.firwin(1000, [b[0], b[1]], pass_zero=False,
                                fs=1000) for b in band_hz]

    # get chopped time index
    ts_chopped = np.arange(time_range[0], time_range[1], 0.001)

    # init dicts to keep track of all channels
    band_mag_chopped = dict()
    band_phs_chopped = dict()
    for b in band_names:
        band_mag_chopped[b] = [None] * len(channel_names)
        band_phs_chopped[b] = [None] * len(channel_names)

    # get bandpassed signal and chop into trials
    for ch in range(len(channel_names)): # TODO: PARALLELIZE!
        print('working on band pass...' + channel_names[ch])
        # load, notch, and bandpass this channel
        mag, phs = get_bandpassed(channel_names[ch], lfp_fname,
                                        ts_long, notch_filts, band_filts)
        # chop by sync points
        mag_chopped = [chop(m.reshape(1, -1), sync_point, time_range)
                       for m in mag]
        phs_chopped = [chop(p.reshape(1, -1), sync_point, time_range)
                       for p in phs]

        # slot in results
        for b in range(len(band_names)):
            band_mag_chopped[band_names[b]][ch] = mag_chopped[b]
            band_phs_chopped[band_names[b]][ch] = phs_chopped[b]

    # cat all channels together for 3D array: sync_points x time x channels
    band_mag_chopped_np = [np.stack(band_mag_chopped[b], axis=2) for b in band_names]
    band_phs_chopped_np = [np.stack(band_phs_chopped[b], axis=2) for b in band_names]

    # save meta data for these channels
    lfp_meta = pd.DataFrame({"ID" : channel_names})

    return band_mag_chopped_np, band_phs_chopped_np, ts_chopped, lfp_meta


def get_bandpassed(chname, fname, ts, notch_filts, band_filts):
    """
    Get mag and phase for bandpassed LFP channel.


    Parameters:
    ----------
    chname : string
        channel ID
    lfp_name : string
        path to LFP data
    ts : np vector
        time stamps for LFP timeseries (in seconds)
    notch_filts : list
        notch filters
    band_filts : list
        bandpass filters

    Returns:
    -------
    mag : list
        np vectors with magntiude of signal in each band_filts
    phs : list
        np vectors with phase of signal in each band_filt

    """

    # load lfp channel
    data = mat73.loadmat(fname, only_include=chname)
    channel = data[chname]

    # apply notch filters serially
    for notch in notch_filts:
        channel = signal.filtfilt(notch[0], notch[1], channel)

    # apply each band pass separately # TODO: parallelize these steps by band!
    bandpassed = [signal.filtfilt(band, 1, channel)
                  for band in band_filts]

    # get analytic signal
    analytic = [signal.hilbert(b) for b in bandpassed]

    # get magnitude, smooth with 50ms boxcar
    mag_raw = [train_to_fr(np.abs(a)) for a in analytic]
    mag = [stats.zscore(m) for m in mag_raw]

    # get phase
    phs = [np.angle(a) for a in analytic]

    return mag, phs
