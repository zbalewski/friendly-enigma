function convert_raw_lfp(varargin)
% convert_raw_lfp()
% convert_raw_lfp(data_path)
% save raw lfp (.pl2) to .mat; data_path is optional
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
addpath('functions', 'Matlab Offline Files SDK/')

% use input as starting path
if length(varargin)==1 & ischar(varargin{1}) & exist(varargin{1})==7
    start_path = varargin{1};
else
    start_path = '../data';
end

out_path = [start_path,'_clean'];
if ~exist(out_path)
    mkdir(out_path)
end

%% load plexon lfp .pl2 files
[file_lfp,path_lfp] = uigetfile(fullfile(start_path, '*.pl2'),...
    'Select Plexon LFP files','MultiSelect','on');
n_lfp = count_files(file_lfp);
if n_lfp==1
    file_lfp = {file_lfp};
end

%% convert lfp .pl2 --> .mat
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

end
end
