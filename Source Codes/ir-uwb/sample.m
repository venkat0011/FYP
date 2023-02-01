% this will be the offical script 
%% Reading the CSV File
function likelystates = IR_UWB_function(seat_location)
close all
try
tic
data =  csvread('z:\radar_x.csv'); % later change this location so it can get the right excel from the rpi
%% Converting the file into complex numbers
recieved_signal = data(:,1:141) +1j*data(:,142:end);
count = size(recieved_signal);
count = count(1);
%% Clutter removal
alpha = 0.95; 
clutter_signal = zeros(count,141);
clutter_signal(1,:) = recieved_signal(1,:);
for i = 2:count
    clutter_signal(i,:) = (alpha .*clutter_signal(i-1,:)) + ( (1-alpha) .* recieved_signal(i,:) ); % this is CK
                         
end
clean_signal = recieved_signal - clutter_signal ;

%% Advanced Clutter Suppression
for i=1:count
    envelope_recieved_signal = abs(hilbert( abs(recieved_signal(i,:))));
    envelope_clean_signal = abs(hilbert( abs(clean_signal(i,:)))) ;
    %min max normalisation
    envelope_recieved_signal = (envelope_recieved_signal -min(envelope_recieved_signal)) ...
                                / ( max(envelope_recieved_signal) -min(envelope_recieved_signal));
                            
    envelope_clean_signal = (envelope_clean_signal -min(envelope_clean_signal)) ...
                                / ( max(envelope_clean_signal) -min(envelope_clean_signal));
    % the imaginary part of the clean signal is the envelope 
    envelope_distance_matrix = [envelope_recieved_signal;envelope_clean_signal];
    application_ratio = min(envelope_distance_matrix)./ (envelope_recieved_signal+10^(-10)) ; % application ratio needs to be 0 to 1 
    clutter_signal(i+1,:) = (application_ratio .* clutter_signal(i,:)) ...
                             + ( (1-application_ratio) .* recieved_signal(i,:));
 end
clean_suppressed = recieved_signal - clutter_signal(2:end,:);

envelope_clean_signal=  envelope(abs(clean_suppressed));

%% distance compensation
envelope_clean_signal = envelope_clean_signal .*(1:141);

%% CFAR ALGO on fast time
rng(42);
Z = envelope_clean_signal;
Z = Z .' ;
Ntraining =34  ; 

Nguard = 4;
Pfa_goal = 10 ^(-1); 
detector = phased.CFARDetector('Method','CA',...
    'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
    'ProbabilityFalseAlarm',Pfa_goal,"Rank",10,...
    'ThresholdFactor','Auto');

Z_detect = detector(Z,1:141);
Z_detect = Z_detect .' ;
detected_signal = Z_detect .* envelope_clean_signal ;

figure;
imagesc((detected_signal));
%% need to fill up the detection 
% for each sample find the locations of the peak -> if the next sample does
% not have any peak at all ( KEY POINT ANY PEAK AT ALL ) then use the
% previous result
% %% Peak Detection Algo
% temp_array = zeros(length(detected_signal),1);
% for k= 2:length(detected_signal)
%     [peaks,idx] = findpeaks(abs(detected_signal(k,:)));
%     temp_array(k,1) = length(peaks) ; % gives us the number of humans at each sample
% end
% number_of_peopleDetected = median(temp_array);
% 
% % this will give us the total number of people detected in the space -> for
% % each of these people we need to see to look into their state transition
% % diagram 

%% pose estimation
% create a list of seats 
% the buffer region will be 10cm radius 
index_count =  1;
% seat_location = [175 600]; % the seat location might not be exact detection so we have to give a leeway of 10%
max_seat_location = seat_location+10;
min_seat_location = seat_location-10;
buffer = 5;
step_size = 2;
seat_observation = ones(floor(count/step_size),2* length(seat_location))  ;
% the first step is to get the observed states out -> to do so we need to
% do a subsampling, in the paper they took the average of the 5 second
% window and mapped it into one of the 3 states 
for i = 1:step_size:count-step_size
    sub_array = detected_signal(i:i+step_size,:) ; % it will be a moving window of 5 seconds
    % if there are multiple objects and multiple seats it might not be so
    % relevant to find the average
    % each observation is a tuple of the first sample and the last sample
    % the observation can fall into 0,1,2 o being centre area, 1 being
    % buffer are and 2 being other
    
    [dummy,first_detected_location] = findpeaks(sub_array(1,:));
    [dummy1,last_detected_location] = findpeaks(sub_array(step_size,:));
    % if we assume that people are the ones with the higher signal then we
    % can use from the number of people detected, in the event there is
    % alot of people

    if(length(first_detected_location) < length(seat_location))
        first_detected_location = padarray(first_detected_location, [0 length(seat_location)], ...
                                    0,'post');
    end
    if(length(last_detected_location) < length(seat_location))
        last_detected_location = padarray(last_detected_location, [0 length(seat_location)], ...
                                    0,'post');
    end
  

    first_detected_location =  first_detected_location .* 5;
    last_detected_location =  last_detected_location .* 5;
    % first and last detected location will now be in an array format, and
    % we need to create multiple observation table for each seat
    tuple = []; 
    % so this creates an issue if the noise is infront it will take the first detected person ( noise) 
        for seat = 1: length(seat_location)
            first_min_difference = inf;
            last_min_difference = inf;
            first_index = 1;
            last_index = 1;
            for index = 1:length(first_detected_location)
                first_difference = abs(seat_location(seat) - first_detected_location(index));
                if(first_difference<first_min_difference)
                    first_index = index;
                    first_min_difference = first_difference;
                end
            end
            for index = 1:length(last_detected_location)
                last_difference = abs(seat_location(seat) - last_detected_location(index));
                if(last_difference<last_min_difference)
                    last_index = index;
                    last_min_difference = last_difference;
                end
            end
            
            if(first_detected_location(first_index) > max_seat_location(seat)+buffer | first_detected_location(first_index)< min_seat_location(seat)-buffer)
                tuple(2*seat-1) = 3 ;
            elseif( first_detected_location(first_index) >= min_seat_location(seat) & first_detected_location(first_index) <= max_seat_location(seat))
                    tuple(2*seat-1) = 1;
            else
                tuple(2*seat-1) = 2;
            end

            if(last_detected_location(last_index) > max_seat_location(seat)+buffer | last_detected_location(last_index)< min_seat_location(seat)-buffer)
                tuple(2*seat) = 3 ;
            elseif( last_detected_location(last_index) >= min_seat_location(seat) & last_detected_location(last_index) <= max_seat_location(seat))
                    tuple(2*seat) = 1;
            else
                tuple(2*seat) = 2;
            end
        end
    seat_observation(index_count,:) = tuple;
    index_count = index_count+1;
    

    
end

disp(seat_observation)
% observed states are done, next is to create the hidden markov model 
% training the hidden markov model will require the labelled states -> we
% need to get the transmission and emission prob
% for training the hidden markov model we need instances of observed data
% and the actual data so we need to compile these results into a excel
% sheet and do the training 
%%
% reading in transmission and emission prob
TRANS = readmatrix("TRANS_EST.txt");
EMIS = readmatrix("EMIS_EST.txt");
% need to do the likely states for each seats 
for i= 1:length(seat_location)
    seat_observation_sample = seat_observation(:,2*i -1:2*i);
    seat_observation_sample  = seat_observation_sample .' ;
    likelystates(i,:) = hmmviterbi(seat_observation_sample, TRANS, EMIS);
end




% %% Localisation of Stationary Subhjects
% clean_detections = detected_signal >0;
% if(number_of_peopleDetected > 0)
%     temp_array1 = sum(clean_detections)/length(clean_detections) ;
%     for i =1: number_of_peopleDetected
%         [a,b] = max(temp_array1);
%         locations(i,1) = b * 5;
%         temp_array1(b-5:b+5) = 0;
%     end
toc
catch 
end
end