%pkg load signal

file1 = "outputFile1.txt";


colorspec = {[0.4 0 0.8]; [0.4 0.8 0]; [0.4 0.7 0.7]; ...
  [0 0.4 0.8]; [0.8 0.4 0]; [0.7 0.4 0.7]; ...
  [0.8 0 0.4]; [0 0.8 0.4]; [0.7 0.7 0.4]; ...
  [0 0 0.7]; [0 0.7 0]; [0.7 0 0]};

colorspec_light = {[0.5 0.2 1]; [0.5 1 0.2]; [0.5 0.9 0.9]; ...
  [0.2 0.5 1]; [1 0.5 0.2]; [0.9 0.5 0.9]; ...
  [1 0.2 0.5]; [0.2 1 0.5]; [0.9 0.9 0.5]; ...
  [0.2 0.2 0.9]; [0.2 0.9 0.2]; [0.9 0.2 0.2]};

graphics_toolkit gnuplot;
%hold on;

C1 = csvread(file1);
size(C1)


loglog(C1(:,1) , C1(:,2),  'LineWidth', 3 , 'Color', colorspec_light{mod(1,12)+1});

%axis([C2(1,1) C2(end,1) min(min(C2))*1.1 max(max(C2))*1.1]);
xlabel('delay variance [%]');
ylabel('components [-] ');
legend(
'50 ps',
'location', 'northwest');
title('Requirements for 1 ps static accuracy');
print('-dpdf', '-color', fullfile(pwd, 'plot.pdf'));

