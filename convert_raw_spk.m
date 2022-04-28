function convert_raw_spk(varargin)
% convert_raw_spk() 
% convert_raw_spk(data_path)
% save raw spk (.pl2) to .mat; data_path is optional
%
% INPUT:
%   data_path - if empty or invalid, File Open dialog to default '../data'
%               if valid, File Open dialog to data_path
%               if valid path, will
%
% OUTPUT:
%   None (.mat saved to file)
%
%% paths
addpath('matlab', 'matlab/Matlab Offline Files SDK/')

% use input as starting path
if length(varargin)==1 & ischar(varargin{1}) & exist(varargin{1})==7
    start_path = varargin{1};
else
    start_path = 'data';
end

out_path = [start_path,'_clean'];
if ~exist(out_path)
    mkdir(out_path)
end

%% load plexon spk .pl2 files
[file_spk,path_spk] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon SPK unit files','MultiSelect','on');
n_spk = count_files(file_spk);
if n_spk==1
    file_spk = {file_spk};
end

%% convert spk .pl2 --> .mat
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
