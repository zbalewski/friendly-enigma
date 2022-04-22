function [bhvfiles, lfpfiles, spkfiles] = convert_raw_data(varargin)
% [bhvfiles, lfpfiles, spkfiles] = convert_raw_data(data_path) -- save raw
% behavior (.bhv2), lfp & spikes (.pl2) to .mat; data_path is optional
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
%% select files through gui: (1) behavior, (2) LFP, (3) spikes
if length(varargin)==1 & ischar(varargin{1}) & exist(varargin{1})==7
    start_path = varargin{1};
else
    start_path = '../data';
end

out_path = [start_path,'_clean'];
if ~exist(out_path)
    mkdir(out_path)
end

% (1) behavior: expecting monkeylogic .bhv2
[file_bhv,path_bhv] = uigetfile(fullfile(start_path, '*.bhv2'),...
    'Select MonkeyLogic behavior files','MultiSelect','on');

% (2) lfp: expecting plexon .pl2
[file_lfp,path_lfp] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon LFP files','MultiSelect','on');

% (3) labeled spikes: expecting plexon .pl2
[file_spk,path_spk] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon SPK unit files','MultiSelect','on');

%% (1) convert behavior .bhv --> .mat
if ~path_bhv
    disp('behavior: skip because no file selected')
else
    disp('behavior: converting to .mat')
    parfor f = 1:length(file_bhv)
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
if ~path_lfp
    disp('lfp: skip because no file selected')
else
    disp('lfp: converting to .mat')
end
%% (3) convert spk .pl2 --> .mat
if ~path_spk
    disp('spk: skip because no file selected')
else
    disp('spk: converting to .mat')
end
end

