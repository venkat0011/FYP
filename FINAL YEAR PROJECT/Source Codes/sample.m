
% this is the source code to read the ir_uwb sensors

% the steps to make=================================================
%1. IQR downconversion -> this gives the signal as a complex signal
%2. Low pass filter ( not too sure if it is already in the reciever)
%3. ADC -> it should be in adc format cos we have discrete values in, refer
%to documentation , it already has a adc it uses swept threshold principle
%So look into that and what it means and why is it good
% At the documentation side there is an optional downconversion into I/Q
% and filtering and this is what the radar that was given to us was setup
% up
% so based on prof luos paper all the steps have been done, but there is
% multipath or clustering seen -> so we have to remove these clusters using
% background subtraction 
% SIGNAL PROCESSING======================================================
% The signal recieved is with noise and what we want to detect are just big
% movements like from sitting to standing. So we will be using a loopback
% filter to remove the background, and we get is only the parts were
% changes were experienced , and the alpha for it is 0.8 -> maybe closer to
% 0.9 cos we still want to detect humans

%testing  out signal subtraction=========================================
% clear;
% close all;
% data =  csvread('stationary_human_part1.csv');
% data2 = csvread('stationary_human_part2.csv');
% data_complex = data(:,1:141)+1j*data(:,142:end);
% data_complex2 = data2(:,1:141)+1j*data2(:,142:end);
% data_complex = abs(data_complex(1:599,:) - data_complex2);
% figure;
% imagesc(abs(data_complex));
% 
% figure;
% amplitude = abs(data_complex(400,:));
% plot(amplitude)
%==========================================================================


% use clean signal for the ft

% Z = wdenoise(abs(clean_signal));
% figure;
% imagesc(Z)
% figure;
% imagesc(abs(clean_signal));

 a = abs(clean_signal(10,:));
 a = a.' ;
 Ntraining = 34  ; % 20% of 141 to train -> got from matlab 

Nguard = 4;
Pfa_goal = 10 ^(-4); 
% the pfa is extracted from 
detector = phased.CFARDetector('Method','CA',...
    'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
    'ProbabilityFalseAlarm',Pfa_goal,...
    'ThresholdFactor','Auto');
 for i =2:2:130
    detector.release();
    detector.NumTrainingCells = i;
    test_detect = detector(a,1:141) ;
    test_detect = test_detect .' ;
    prob = sum(test_detect)/length(test_detect);
    array(count,1) = max(prob);
    array(count,2) = i;
    count = count+1;
 end
figure;
plot(array(:,2),array(:,1)) ;
 























% % z = clean_signal(2:10,:)
% % z = abs(z) .^2
% % local_max = z(1)
% % peak_index = 1
% % for i =1:141
% %     if(z(i) > local_max)
% %         peak_index = i
% %         local_max = z(i)
% %     end
% % end
% % 
% % detector = phased.CFARDetector('NumGuardCells',4,...
% %     'NumTrainingCells',4,'ProbabilityFalseAlarm',1e-6);
% % 
% % rng(1000);
% % a = detector(z,2) ;
% 
% 
% rng(2022);
% Z = abs(clean_signal).^2;
% Ntraining = 80;
% Nguard = 2;
% Pfa_goal = 10 ^(-5); 
% % the pfa is extracted from 
% detector = phased.CFARDetector('Method','OS',...
%     'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
%     'ProbabilityFalseAlarm',Pfa_goal,'Rank',5);
% Z_detect = detector(Z,1:length(Z));
% %Z_detect = Z_detect .' ;
% % 
% 
% figure;
% imagesc(abs(Z_detect .* clean_signal));

% detector = phased.CFARDetector('NumGuardCells',2,...
%     'NumTrainingCells',20,'ProbabilityFalseAlarm',1e-3);
% Ntrials = 100;
% variance = 0.25;
% Ncells = 23;
% inputdata = sqrt(variance/2)*(randn(Ncells,Ntrials)+1j*randn(Ncells,Ntrials));
% Z = abs(inputdata).^2;
% Z_detect = detector(Z,78); % this performs CFAR on fast time

% 
% rng(2022);
% Z = abs(clean_signal(50,:)).^2;
% Ntraining = 100;
% Nguard = 2;
% Pfa_goal = 10 ^(-5); 
% %the pfa is extracted from 
% detector = phased.CFARDetector('Method','OS',...
%     'NumTrainingCells',Ntraining,'NumGuardCells',Nguard,...
%     'ProbabilityFalseAlarm',Pfa_goal,'Rank',5);
% Z_detect = detector(Z,1);

% figure;
% imagesc(abs(Z_detect .* clean_signal(50:));
% cfar = phased.CFARDetector('NumTrainingCells',20,'NumGuardCells',2);
% npower = db2pow(-10);  % Assume 10dB SNR ratio
% rs = RandStream('mt19937ar','Seed',2010);
% Npoints = 1e4;
% rsamp = randn(rs,Npoints,1)+1i*randn(rs,Npoints,1);
% ramp = linspace(1,10,Npoints)';
% xRamp = abs(sqrt(npower*ramp./2).*rsamp).^2; % notice this is as column vector 


% 
% load sunspot.dat
% year = sunspot(:,1); 
% relNums = sunspot(:,2);
% [peaks,idx] = findpeaks(relNums,year);
% for i = idx
%     disp(i);
% end
% xlabel('Year')
% ylabel('Sunspot Number')
% title('Find All Peaks')




%CFAR ON A 1 ROW BY 1 ROW BASIS====================================
% Z_detect = [] ;
% for i = 1: length(Z)
%     Z_detect(i,:) = detector(Z(:,i),1:141);
%     
% end
% % 
% detected_signal = Z_detect .* clean_signal ;
% figure;
% imagesc(abs(detected_signal));
%======================================================================

a = clean_detected_signal > 0 ;
b = [];
for i = 1:141
    b(:,i) = a(:,i) * i ;
end