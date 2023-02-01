clear ;
close all;
%% reading in the binary file
% rawDataReader('testing.setup.json','stationary_50_raw', 'stationary_50_fft', 1);
%% loading the radar cube
data = load('radarCube.mat');
data = data.radarCube.data;

% the data being read here is the range fft -> look into what is range fft
% the data is a cell structure with x number of frame, each frame consist
% of 128*y*256. Y here represents the number of reciver channels
for i = 1:length(data) % this will iterate through all the frames
    reciever = cell2mat(data(i));
    % extract all the 4 reciever, but here we will be just trying with 1
    reciever_1 = reshape(reciever(:,1,:),[128,256]);
    % each frame sends out 128 chirps, these chirps are of increasing
    % frequency. Each chirp is sampled 256 times therefore each chirp has
    % 256. After range FFT, these 256 bins represent 50m, so each bin will
    % represent 0.1952m or just 19.52cm
    
    % after performing range fft -> the x axis should represent the range (
    % 1:256) but the y should reflect the db 
    
    % converting each value of the range fft into the db equivalent
%     reciever_1 = 20 .* log10(abs(reciever_1)) ;
        
      
    
end
% when reading the matfile, each frame has 128 

%% the cfar that was used in the mmwave is 2d cfar -> for 2d cfar we need to make use of range doppler
% 2d cfar is similar to 2d fft where do fft on the slow time then do fft on
% the fast time
% here we will first perform fft on the fast time -> range 
% and do another cfar on the slow time -> doppler and do a and gate 
% so if both is detected then it is considered a target located at a
% specific range with a certain velocity 

% cfar on the range
range_doppler = fft(reciever_1,[],1);
%%
Ntraining =32  ; 

Nguard = 8;
Pfa_goal = 10 ^(-5); 
detector = phased.CFARDetector('Method','CA',...
    'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
    'ProbabilityFalseAlarm',Pfa_goal,...
    'ThresholdFactor','Auto');

range_detect = detector(abs(range_doppler)',1:256);
range_detect = range_detect .' ;

detector.release();
doppler_detect = detector(abs(range_doppler),1:128);


detected_result = doppler_detect & range_detect ;
% multiplying 
% % first concatenate all the reciever 
% % perform fft on the slow time -> to get range doppler image then we can
% 
% cfar2D = phased.CFARDetector2D('GuardBandSize',8,'TrainingBandSize',32,...
%   'ProbabilityFalseAlarm',10e-4);
% detect = cfar2D(abs(range_doppler),[40 100]' );
%%