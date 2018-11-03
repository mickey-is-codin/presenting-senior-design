clc;
close all;

%% Import CSVs Created from Python Script
[overall_data, small_data, der1_data, der2_data] = import_csvs();

%% Make arrays for each metric from the session
%% Full time of session
still_full = overall_data(:,1);
still_music_full = overall_data(:,2);
hand_up_full = overall_data(:,3);
hand_down_full = overall_data(:,4);
walking_full = overall_data(:,5);
running_full = overall_data(:,6);
after_sprint_full = overall_data(:,7);
tapping_fingers_full = overall_data(:,8);
tapping_foot_full = overall_data(:,9);
flexing_full = overall_data(:,10);

%% Shortened time section of session
still_small = small_data(:,1);
still_music_small = small_data(:,2);
hand_up_small = small_data(:,3);
hand_down_small = small_data(:,4);
walking_small = small_data(:,5);
running_small = small_data(:,6);
after_sprint_small = small_data(:,7);
tapping_fingers_small = small_data(:,8);
tapping_foot_small = small_data(:,9);
flexing_small = small_data(:,10);

%% All first derivatives of signals
still_der1 = der1_data(:,1);
still_music_der1 = der1_data(:,2);
hand_up_der1 = der1_data(:,3);
hand_down_der1 = der1_data(:,4);
walking_der1 = der1_data(:,5);
running_der1 = der1_data(:,6);
after_sprint_der1 = der1_data(:,7);
tapping_fingers_der1 = der1_data(:,8);
tapping_foot_der1 = der1_data(:,9);
flexing_der1 = der1_data(:,10);

%% All second derivatives of signals
still_der2 = der2_data(:,1);
still_music_der2 = der2_data(:,2);
hand_up_der2 = der2_data(:,3);
hand_down_der2 = der2_data(:,4);
walking_der2 = der2_data(:,5);
running_der2 = der2_data(:,6);
after_sprint_der2 = der2_data(:,7);
tapping_fingers_der2 = der2_data(:,8);
tapping_foot_der2 = der2_data(:,9);
flexing_der2 = der2_data(:,10);

%% Begin Single Waveform Analysis
analysis_signal = tapping_foot_small;

%% Get Peak/Trough Values and Locations
[sys_peak_vals, sys_peak_locs] = get_systolic_peaks(analysis_signal);
[notch_pks, notch_locs] = dicrotic_notch_logic(analysis_signal, sys_peak_locs);
[trough_pks, trough_locs] = trough_finding(analysis_signal);

%% Plot Metrics
figure();
suptitle('Signal Analysis for BVP Waveform');

subplot(3,1,1);
hold on;
plot(analysis_signal);
for i = 1:length(sys_peak_locs)
    plot(sys_peak_locs(i),sys_peak_vals(i),'r*');
    plot(notch_locs(i),analysis_signal(notch_locs(i)),'b*');
    plot(trough_locs(i),trough_pks(i),'g*');
end
hold off;
title('Critical Signal Locations');

subplot(3,1,2);
plot(diff(analysis_signal));
title('First Derivative of Signal');

subplot(3,1,3);
plot(diff(diff(analysis_signal)));
title('Second Derivative of Signal');

width=2000;
height=1000;
set(gcf,'units','points','position',[0,500,width,height]);

%% User Defined Tool Functions
%% Systole Peaks
function [peak_vals, peak_locs] = get_systolic_peaks(signal)
    [peak_vals, peak_locs] = findpeaks(signal,'MinPeakProminence',15);
end

%% Diastole Troughs
function [trough_pks, trough_locs] = trough_finding(analysis_signal)
    upside_down = (-1) * analysis_signal;  
    [trough_pks,trough_locs] = findpeaks(upside_down, 'MinPeakProminence', 10);
    trough_pks = (-1) * trough_pks;
end

%% Dicrrotic Notches
function [notch_pks, notch_locs] = dicrotic_notch_logic(signal, sys_locs)
    [notch_pks, notch_locs] = notch_algorithm(signal);
end

function [notch_pks, notch_locs] = notch_algorithm(signal)
    % Dicrotic Notch Algorithm
    [sys_peaks,sys_locs] = findpeaks(diff(signal), 'MinPeakHeight', 10); % Larger threshold
    [both_peaks,both_locs] = findpeaks(diff(signal), 'MinPeakHeight', -5, 'MinPeakDistance', 10); % Smaller threshold
    [C, ia] = setdiff(both_locs, sys_locs, 'stable');
    
    notch_locs = both_locs(ia);
    notch_pks = both_peaks(ia);
end

%% Dataset Import Function
function [overall_data, small_data, der1_data, der2_data] = import_csvs()
    overall_path = strcat('./Oct25LabSession/', 'Oct25FullSession.csv');
    overall_data = csvread(overall_path,2,1);
    
    small_path = strcat('./Oct25LabSession/', 'Oct25SmallSegment.csv');
    small_data = csvread(small_path,2,1);
    
    der1_path = strcat('./Oct25LabSession/', 'Oct25FirstDerivatives.csv');
    der1_data = csvread(der1_path,2,1);
    
    der2_path = strcat('./Oct25LabSession/', 'Oct25SecondDerivatives.csv');
    der2_data = csvread(der2_path,2,1);
end