default_csv = dir('default-*.csv');

temp = load(default_csv(1).name);
default_data = zeros([size(temp) length(default_csv)]);
default_data(:,:,1) = load(default_csv(1).name);

for i = 2:length(default_csv)
  default_data(:,:,i) = load(default_csv(i).name);
end

figure
hold on
#x = default_data(:,3,1)
#y = default_data(:,1,1)
#plot(x,y)

col = varycolor(length(default_csv));
for i = 1:length(default_csv)
  plot(default_data(:,3,i),default_data(:,1,i), 'Color', col(i,:))
end
#mean(default_data(:,1,:),2)
#plot(mean(default_data(:,3,:),2),mean(default_data(:,1,:),2), '.k')
print('test.png','-dpng')
