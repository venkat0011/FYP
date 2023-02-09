clear ;
close all;
%% reading in the binary file
% rawDataReader('testing.setup.json','stationary_50_raw', 'stationary_50_fft', 1);
%% loading the radar cube
data = load('Human_Chair_Samples/person_250_fft.mat');
data = data.radarCube.data;

% the data being read here is the range fft -> look into what is range fft
% the data is a cell structure with x number of frame, each frame consist
% of 128*y*256. Y here represents the number of reciver channels
for i = 1:length(data) % this will iterate through all the frames
    reciever = cell2mat(data(i));
    % extract all the 4 reciever, but here we will be just trying with 1
    reciever_1 = reshape(reciever(:,1,:),[128,256]);
    reciever_2 = reshape(reciever(:,2,:),[128,256]);
    reciever_3 = reshape(reciever(:,3,:),[128,256]);
    reciever_4 = reshape(reciever(:,4,:),[128,256]);
    % each frame sends out 128 chirps, these chirps are of increasing
    % frequency. Each chirp is sampled 256 times therefore each chirp has
    % 256. After range FFT, these 256 bins represent 50m, so each bin will
    % represent 0.1952m or just 19.52cm
    recieved_sum = reciever_1+ reciever_2+reciever_3+reciever_4;
    

    range_doppler = fft(recieved_sum,[],1);
    Ntraining =32  ; 

    Nguard = 8;
    Pfa_goal = 10 ^(-5); 
    detector = phased.CFARDetector('Method','CA',...
        'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
        'ProbabilityFalseAlarm',Pfa_goal,...
        'ThresholdFactor','Auto');
    range_detect = detector(abs(range_doppler)',1:256);
    range_detect = range_detect .' ;
    % is there a need for 2d cfar here ??
    
    detector.release();
    doppler_detect = detector(abs(range_doppler),1:128);
    detected_result = doppler_detect & range_detect ;
    
    %% after the detected signal is obtained we need to perform peak detection 
    [doppler_index,range_index] = find(detected_result==1); 
    % when there is mutliple targets detected, the range_index will be a
    % list
    
    % there might be duplicates 
    range_index = unique(range_index);
    
    
    
    % we will iterate through this list of range and obtain the 5
    % properties in the fft range signal and append them to a list 
    % this method will work
%     for range = range_index
%         % for each chirp the 
%     end
    
          
    
end


%% the cfar that was used in the mmwave is 2d cfar -> for 2d cfar we need to make use of range doppler
% 2d cfar is similar to 2d fft where do fft on the slow time then do fft on
% the fast time
% here we will first perform fft on the fast time -> range 
% and do another cfar on the slow time -> doppler and do a and gate 
% so if both is detected then it is considered a target located at a
% specific range with a certain velocity 
