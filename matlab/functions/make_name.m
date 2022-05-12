function new_name = make_name(unit_names, channel_name, u)
% [new_name] = make_name(unit_names, channel_name, u)
% make a unique unit name from channel id and unit label
%
% INPUT:
%   unit_name - cell array of unit names so far in the session
%   channel_name - string, current channel id
%   u - int, current unit (ref a, b, etc in OfflineSorter)
%
% OUTPUT:
%   new_name - string, unique unit label
%


% OfflineSorter reference for u = 1, 2, ...
unit_letters = {'a','b','c','d','e','f'};

% default name: channel id and unit letter idenifier
new_name = [channel_name, unit_letters{u}];

% if default name exists, repeat letter until name is unique (these repeats
% can happen when resorting old data, or using both positive and negative
% threshold crossings)
while sum(strcmp(new_name, unit_names)) > 0 % already exists! 
    new_name = [new_name, unit_letters{u}];
end

end

