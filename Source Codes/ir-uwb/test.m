%this will be the script to train the hidden markov model
%% Reading the CSV File
% clear;
% close all;
% % what we need is to predict the transmission and emission 
% % store these transmission and emission somewhere, either in excel or
% % somewhere so we can read it everytime the code runs
% 
% HMMtrainingdata = readtable('HMM_trainingdata.csv');
% Observed_state1 = HMMtrainingdata.Var1;
% Observed_state2 = HMMtrainingdata.Var2;
% for i = 1: length(Observed_state1)
%     seq(i,:) = [ Observed_state1(i) Observed_state2(i) ];
% end
% 
% actual_state = HMMtrainingdata.Var3 .' ;
% seq= seq.';
% 
% [TRANS_EST, EMIS_EST] = hmmestimate(seq, actual_state) ;
% writematrix(TRANS_EST);
% writematrix(EMIS_EST);

% take note 2 is seat is taken 





state = sample( [50]);
