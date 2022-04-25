function load_spk_pl2(lfp_pl2, out_file)
% [spkdata] = load_spk_pl2(spk_pl2)
% load raw spikes (.pl2) and convert to .mat
%
% INPUT:
%   lfp_pl2 - filename for raw pl2; has 1kHz LFP signal
%
% OUTPUT:
%   None 
%   (channel names and LFP signal saved directly to out_file)
%
%% get channel names
[~, names] = plx_adchan_names(lfp_pl2);
names = cellstr(names);
channel_names = names(cellfun(@(x) ~isempty(strfind(x,'FP')),names)); % only keep FP channels
Nchannels = length(channel_names);

%% get time stamps of samples
[~, ~, lfp_ts] = plx_ad(lfp_pl2, channel_names{1});

%% get event codes
[~, event_ts, event_codes] = plx_event_ts(lfp_pl2, 'Strobed');

%% save names, time stamps, and events
save(out_file, 'channel_names', 'lfp_ts', 'event_ts', 'event_codes', '-v7.3');

%% cycle through each channel, save 
for ch = 1:Nchannels
    % load lfp channel
    [adfreq,~,~,~,V] = plx_ad(lfp_pl2, channel_names{ch});
    
    % rename and save voltage
    eval([channel_names{ch},'=V; clear(''V'');'])
    save(out_file, channel_names{ch}, '-append');
end         

end

