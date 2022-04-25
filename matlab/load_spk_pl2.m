function load_spk_pl2(spk_pl2)
% [spkdata] = load_spk_pl2(spk_pl2)
% load raw spikes (.pl2) and convert to .mat
%
% INPUT:
%   spk_pl2 - filename for raw pl2; has raw spike times and waveforms
%
% OUTPUT:
%   None
%   (unit names and spike times saved directly to out_file)
%
%% get channel names
[Nchannels, names] = plx_chan_names(spk_pl2);
names = cellstr(names);

%% save event codes
[~, event_ts, event_codes] = plx_event_ts(lfp_pl2, 'Strobed');
save(out_file, 'event_ts', 'event_codes', '-v7.3')

%% cycle through each channel looking for units
unit_names = {};

for ch = 1:Nchannels
    for u = 1:6 % look for up to 6 units/channel
        
        % get spike times
        [~, ts] = plx_ts(spk_pl2, ch, u); 
        
        
        if ts==-1 % exceeds # of units on this channel; 
            break
            
        else % we got a unit!
            % define unique name
            new_name = make_name(unit_names, names{ch}, u);
            unit_names{end+1, 1} = new_name;
            
            % rename and save spike times
            eval([new_name,'=ts; clear(''ts'');'])
            save(out_file, new_name, '-append')
            
            % TODO: use 'plx_waves' to read waveforms...
        end
    end
end
            
save(out_file, 'unit_names', '-append')
 
end

