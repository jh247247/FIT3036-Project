function plotOutput(prefix)

  graphics_toolkit gnuplot;

  default_csv = dir(strcat(prefix,'-*.csv'));

  # load one to figure out
  temp = load(default_csv(1).name);
  default_data = zeros([size(temp) length(default_csv)]);
  default_data(:,:,1) = load(default_csv(1).name);

  for i = 2:length(default_csv)
    default_data(:,:,i) = load(default_csv(i).name);
  end

  fig = figure('Visible','off')
  hold on

  col = varycolor(length(default_csv));
  for i = 1:length(default_csv)
    plot(default_data(:,2,i),default_data(:,1,i), 'Color', col(i,:))
  end
  print(fig, strcat(prefix,'.png'),'-dpng')

  close all

  defaultAvg = mean(default_data,3);
  fig = figure('Visible','off')
  plot(defaultAvg(:,2), defaultAvg(:,1),'.k')
  hold on
  plot(defaultAvg(:,2), defaultAvg(:,5),'r')
  plot(defaultAvg(:,2), defaultAvg(:,6),'g')
  print(fig, strcat(prefix,'-avg.png'),'-dpng')

endfunction
