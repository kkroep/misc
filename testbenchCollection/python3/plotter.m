%pkg load signal

file1 = "outputFile1.txt";
file2 = "outputFile2.txt";
file3 = "outputFile3.txt";


colorspec = {[0.4 0 0.8]; [0.4 0.8 0]; [0.4 0.7 0.7]; ...
  [0 0.4 0.8]; [0.8 0.4 0]; [0.7 0.4 0.7]; ...
  [0.8 0 0.4]; [0 0.8 0.4]; [0.7 0.7 0.4]; ...
  [0 0 0.7]; [0 0.7 0]; [0.7 0 0]};

colorspec_light = {[0.5 0.2 1]; [0.5 1 0.2]; [0.5 0.9 0.9]; ...
  [0.2 0.5 1]; [1 0.5 0.2]; [0.9 0.5 0.9]; ...
  [1 0.2 0.5]; [0.2 1 0.5]; [0.9 0.9 0.5]; ...
  [0.2 0.2 0.9]; [0.2 0.9 0.2]; [0.9 0.2 0.2]};

graphics_toolkit gnuplot;
hold on;

C1 = csvread(file1);
C2 = csvread(file2);
C3 = csvread(file3);


plot(C1(:,1) , C1(:,2),  'LineWidth', 3 , 'Color', colorspec_light{mod(1,12)+1});
plot(C2(:,1) , C2(:,2),  'LineWidth', 3 , 'Color', colorspec_light{mod(1,12)+2});
plot(C3(:,1) , C3(:,2),  'LineWidth', 3 , 'Color', colorspec_light{mod(1,12)+3});


hold off;

%axis([C2(1,1) C2(end,1) min(min(C2))*1.1 max(max(C2))*1.1]);
set(gca,'fontsize',14);
xlabel('delay variance [%]');
ylabel('components*counts [-] ');
legend(
'\mu_c = 25  ps',
'\mu_c = 50  ps',
'\mu_c = 100 ps',
'location', 'northwest');
title('Requirements for 1 ps static accuracy');
print('-dpdf', '-color', fullfile(pwd, 'plot.pdf'));

