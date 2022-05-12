# friendly-enigma
final project AY250: ephys preprocessing pipeline (for Wallis lab)

## Overview
0. Convert raw data
1. Extract task event time stamps (to sync neural data)
2. next step


## Details

### 0. Convert raw data

During a typical session, we record 3 types of data concurrently:
1. Behavior: the task events and subject responses are controlled by the MATLAB Toolbox [MonkeyLogic](https://monkeylogic.nimh.nih.gov/); task events saved in .bhv2
2. Local field potentials (LFP): voltage signals < 250Hz are sampled at 100Hz and recorded with [Plexon's OmniPlex system](https://plexon.com/plexon-systems/omniplex-neural-recording-system/); continuous data saved in .pl2
3. Spiking data (SPK): voltage signals > 250Hz are sampled at 40kHz and recorded with [Plexon's OmniPlex system](https://plexon.com/plexon-systems/omniplex-neural-recording-system/); waveforms (4 st. dev threshold crossings) are manually sorted into unique sources (neurons) with [Plexon's OfflineSorter](https://plexon.com/products/offline-sorter/); threshold crossing timestamps saved in .pl2

To sync these data streams, we send duplicate task event codes from the PC controlling behavior to the PC recording neural data.

These unique filetypes were designed to for MATLAB and Windows machines, and are not easily accessible with Python. To avoid spending my entire project on just opening the raw data in Python, I first convert everything to .mat files in MATLAB:
```
matlab/convert_raw_bhv.m  % select behavioral files
matlab/convert_raw_lfp.m  % select LFP files
matlab/convert_raw_spk.m  % select spiking files
```
(See small sample files in ephyspipe/tests/sample_data for reference.)

### 1. Extract task event time stamps (to sync neural data)
```import ephyspipe.behavior as bhv```

Load in the raw behavioral data:

```
bhv_data = bhv.load_raw_bhv([path_to_bhvfile_A, path_to_bhvfile_B])  # input list of paths for all behavioral trials from this session
```
and the duplicate event codes from either the LFP or spiking data:
```
pl2_codes = bhv.load_pl2_codes(path_to_spkfile)
```

Extract timestamps for the events (e.g. stimulus onset, reward) you want to use as sync points:
```
code_stimulus = 20  # these are unique to each experiment
sync_timestamps = bhv.get_trial_events(bhv_data, pl2_codes, code_stimulus)
```

### 2. next step



## Example Notebook

For more info, check out the [final project jupyter notebook](https://github.com/zbalewski/python-ay250-homework/tree/main/final_project).
