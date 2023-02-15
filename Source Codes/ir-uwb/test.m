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





% state = sample( [50]);

n = (-10:1:10)';
unitstep = n<=0;
newunitstep = n<=1;
impulse = n==0;
new_impulse = n==1;
x =  (3.^n .*newunitstep) ;
TA_signal = impulse - ( -1 .* x);
proposed_signal = (-3 .* new_impulse) - (-1 .*x) ; 
subplot(3,1,1);stem(n,3.^n .* unitstep);axis on; title("3^n u[-n]");
% subplot(4,1,2);stem(n,x);axis on; title("3^n u[-n-1]");
subplot(3,1,2);stem(n,TA_signal);axis on; title("TA's Signal");
subplot(3,1,3);stem(n,proposed_signal);axis on; title("Proposed signal");
% stem(n,3.^n .* unitstep);
