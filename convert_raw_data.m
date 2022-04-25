function [bhvfiles, lfpfiles, spkfiles] = convert_raw_data(varargin)
% [bhvfiles, lfpfiles, spkfiles] = convert_raw_data(data_path)
% save raw behavior (.bhv2), lfp & spikes (.pl2) to .mat; data_path is optional
%
% INPUT:
%   data_path - if empty or invalid, File Open dialog to default '../data'
%               if valid, File Open dialog to data_path
%               if valid path, will
%
% OUTPUT:
%   bhvfiles - cell array with behavior filenames (.mat)
%
%   lfpfiles - cell array with lfp filenames (.mat)
%
%   spkfiles - cell array with unit spike filenames (.mat)
%
%% add path to Plexon's SDK
addpath('matlab', 'matlab/Matlab Offline Files SDK/')

%% select files through gui: (1) behavior, (2) LFP, (3) spikes
if length(varargin)==1 & ischar(varargin{1}) & exist(varargin{1})==7
    start_path = varargin{1};
else
    start_path = 'data';
end

out_path = [start_path,'_clean'];
if ~exist(out_path)
    mkdir(out_path)
end

% (1) behavior: expecting monkeylogic .bhv2
[file_bhv,path_bhv] = uigetfile(fullfile(start_path, '*.bhv2'),...
    'Select MonkeyLogic behavior files','MultiSelect','on');
n_bhv = count_files(file_bhv);
if n_bhv==1
    file_bhv = {file_bhv};
end

% (2) lfp: expecting plexon .pl2
[file_lfp,path_lfp] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon LFP files','MultiSelect','on');
n_lfp = count_files(file_lfp);
if n_lfp==1
    file_lfp = {file_lfp};
end

% (3) labeled spikes: expecting plexon .pl2
[file_spk,path_spk] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon SPK unit files','MultiSelect','on');
n_spk = count_files(file_spk);
if n_spk==1
    file_spk = {file_spk};
end
%% (1) convert behavior .bhv --> .mat
if path_bhv==0
    disp('behavior: skip because no file selected')
else
    disp('behavior: converting to .mat')
    for f = 1:n_bhv
        out_file = fullfile(out_path,strrep(file_bhv{f}, '.bhv2', '.mat'));
        if exist(out_file)==2
            disp(['...',file_bhv{f},'... .mat exists'])
        else
            disp(['...',file_bhv{f},'... creating .mat'])
            bhvdata = mlread(fullfile(path_bhv, file_bhv{f}));
            save(out_file, 'bhvdata', '-v7.3')
        end
    end
end

%% (2) convert lfp .pl2 --> .mat
if path_lfp==0
    disp('lfp: skip because no file selected')
else
    disp('lfp: converting to .mat')
    for f = 1:n_lfp
        out_file = fullfile(out_path, strrep(file_lfp{f}, '.pl2', '.mat'));
        if exist(out_file)==2
            disp(['...',file_lfp{f},'... .mat exists'])
        else
            disp(['...',file_lfp{f},'... creating .mat'])
            load_lfp_pl2(fullfile(path_spk, file_lfp{f}), out_file);         
        end
end
%% (3) convert spk .pl2 --> .mat
if path_spk==0
    disp('spk: skip because no file selected')
else
    disp('spk: converting to .mat')
    for f = 1:n_spk
       out_file = fullfile(out_path, strrep(file_spk{f}, '.pl2', '.mat'));
       if exist(out_file)==2
           disp(['...',file_spk{f},'... .mat exists'])
       else
           disp(['...',file_spk{f},'... creating .mat'])
           load_spk_pl2(fullfile(path_spk, file_spk{f}), out_file);
       end
    end
end
end

