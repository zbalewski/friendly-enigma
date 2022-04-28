function convert_raw_bhv(varargin)
% convert_raw_bhv() 
% convert_raw_bhv(data_path)
% save raw behavior (.bhv2) to .mat; data_path is optional
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

%% load monkeylogic .bhv2 files
[file_bhv,path_bhv] = uigetfile(fullfile(start_path, '*.bhv2'),...
    'Select MonkeyLogic behavior files','MultiSelect','on');
n_bhv = count_files(file_bhv);
if n_bhv==1
    file_bhv = {file_bhv};
end

%% convert behavior .bhv --> .mat
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

end

