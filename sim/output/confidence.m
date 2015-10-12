function confidence(prefix)
  fnames = dir(strcat(prefix,'-*.csv'));

				# load one to figure out length
  temp = load(fnames(1).name);
  default_data = zeros([size(temp) length(fnames)]);
  default_data(:,:,1) = load(fnames(1).name);

  for i = 2:length(fnames)
    default_data(:,:,i) = load(fnames(i).name);
  end

  m = mean(default_data,3) # get mean of data
  std = std(default_data,0,3)
  plot(m(:,2),m(:,1))

endfunction
