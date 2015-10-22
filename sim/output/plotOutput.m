function plotOutput(prefix,amount)

  graphics_toolkit gnuplot;

  default_csv = dir(strcat(prefix,'-*.csv'));

  # load one to figure out
  temp = load(default_csv(1).name);
  default_data = zeros([size(temp) length(default_csv)]);
  default_data(:,:,1) = load(default_csv(1).name);

  for i = 2:min(length(default_csv),amount)
    default_data(:,:,i) = load(default_csv(i).name);
  end



  con = confidence(prefix, amount);
  index = round(linspace(1,length(con)));

  avgData = mean(default_data,3);
  defaultAvg = mean(con,2);

  fig = figure('Visible','off')
  errorbar(avgData(index,2),avgData(index,1),
	   abs(con(index,1)-con(index,2))/2)
  hold on
  plot(avgData(index,2), avgData(index,1),'.k')
  hold on
  title(['Plot type: ' prefix ' Amount of runs: ' num2str(amount)])
  xlabel('Solar Luminosity')
  ylabel('Temperature (C)')
  plot(avgData(:,2), avgData(:,5),'r')
  ##plot(defaultAvg(:,2), defaultAvg(:,6),'g')
  print(fig, strcat(prefix,'-avg.png'),'-dpng','-r72')

  close all

  fig = figure('Visible','off')
  hold on

  title(['Plot type: ' prefix ' Amount of runs: ' num2str(amount)])
  plot(avgData(index,2), avgData(index,11),'r') # iblack
  #plot(avgData(index,2), avgData(index,10),'dr') # iwhite
  plot(avgData(index,2), avgData(index,9),'k') # black
  plot(avgData(index,2), avgData(index,8),'g') # white
  plot(avgData(index,2), avgData(index,7),'b') # blank
  xlabel('Solar Luminosity')
  ylabel('Amount of type')
  print(fig, strcat(prefix,'.png'),'-dpng','-r72')



endfunction
