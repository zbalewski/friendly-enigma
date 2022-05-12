function n = count_files(file_names)
% n = count_files(file_names)
% count how many files are in file_names
%
% INPUT:
%   file_names - 0 (none), char vector (1), or cell array (>1)
%
% OUTPUT:
%   n - int, # of files
%
%% count how many in file_names
if ischar(file_names)
    n = 1;
elseif iscell(file_names)
    n = length(file_names);
elseif file_names==0
    n = 0;
end
end
