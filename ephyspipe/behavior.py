import mat73
from collections import defaultdict
import numpy as np
import pandas as pd


def load_raw_bhv(bhv_fnames):
    """
    Load raw bhv (.bhv2 saved as .mat) into dict; consolidate
    if split across multiple files (assume alpha order)

    Parameters:
    ----------
    bhv_fnames : list
        File path(s) for behavior data

    Returns:
    -------
    bhv_data : dict
        All task data

    """

    bhv_data = defaultdict(list)

    for f in bhv_fnames:
        print(f)
        data = mat73.loadmat(f)

        data_vars = data["bhvdata"].keys()
        for v in data_vars:
            bhv_data[v] += data["bhvdata"][v]

    return bhv_data


def load_pl2_codes(spk_fname):
    """
    Load task event codes and corresponding time stamps from
    raw spk (.pl2 saved as .mat).

    Parameters:
    ----------
    spk_fname : string
        File path for spk data

    Returns:
    -------
    pl2_codes : dict
        Event codes and timestamps from whole session

    """

    pl2_codes = mat73.loadmat(spk_fname,
                              only_include=["event_codes", "event_ts"])

    return pl2_codes


def get_trial_events(bhv_data, pl2_codes, event):
    """
    For each trial in bhv_data, pull time for this event code
    (-1 if doesn't exist)

    Parameters:
    ----------
    bhv_data : dict
        All task data
    pl2_codes : dict
        Event codes and timestamps from whole session
    event : int
        Event code word

    Returns:
    -------
    timestamps : np vector
        Timestamps corresponding to event within each trial (or -1)

    """

    # cut up trials by default start and stop codes
    start_code = 9
    stop_code = 18

    trial_start = np.where(pl2_codes["event_codes"] == start_code)[0]
    trial_stop = np.where(pl2_codes["event_codes"] == stop_code)[0]

    # check that we have the same number of trials from bhv and pl2 data
    ntr = len(bhv_data["Trial"])
    if trial_start.shape[0] != ntr or trial_stop.shape[0] != ntr:
        raise ValueError("oops! mismatched bhv2 and pl2 trial counts")

    # cycle through all trials, save event time (if exists)
    timestamps = -1 * np.ones(ntr)
    for tr in range(ntr):

        # restrict to event codes in this trial
        codes = pl2_codes["event_codes"][trial_start[tr]:trial_stop[tr]]
        ts = pl2_codes["event_ts"][trial_start[tr]:trial_stop[tr]]

        idx = np.where(codes == event)[0]
        if idx.shape[0] == 1:
            timestamps[tr] = ts[idx]

    return timestamps


def get_trialinfo(bhv_data):
    """
    Pull some trial info.

    Parameters:
    ----------
    bhv_data : dict
        All task data

    Returns:
    -------
    trialinfo : pd dataframe
        trials x features; should expand this...

    """

    # free vs forced trials
    trialtype = [obj["CurrentConditionInfo"][0]["trialtype"] for obj in bhv_data["TaskObject"]]

    # amnt and prob for left and right picture
    amnt_left = [obj["CurrentConditionInfo"][0]["amnt"][0] for obj in bhv_data["TaskObject"]]
    amnt_right = [obj["CurrentConditionInfo"][0]["amnt"][1] for obj in bhv_data["TaskObject"]]

    prob_left = [obj["CurrentConditionInfo"][0]["prob"][0] for obj in bhv_data["TaskObject"]]
    prob_right = [obj["CurrentConditionInfo"][0]["prob"][1] for obj in bhv_data["TaskObject"]]

    # make data frame, and add some useful columns
    trialinfo = pd.DataFrame({"trialtype": trialtype,
                              "amnt_left": amnt_left,
                              "amnt_right": amnt_right,
                              "prob_left": prob_left,
                              "prob_right": prob_right})

    trialinfo["value_left"] = trialinfo["amnt_left"] * trialinfo["prob_left"]
    trialinfo["value_right"] = trialinfo["amnt_right"] * trialinfo["prob_right"]
    trialinfo["value_max"] = trialinfo[["value_left", "value_right"]].max(axis=1)
