function con = confidence(prefix,maxDataSet)
  # returns non-zero if all data lies within 95% confidence interval
  fnames = dir(strcat(prefix,'-*.csv'));
  if(length(fnames) == 0)
    con = 1
    return
  end

				# load one to figure out length
  temp = load(fnames(1).name);
  default_data = zeros([size(temp) length(fnames)]);
  default_data(:,:,1) = load(fnames(1).name);

  for i = 2:min(length(fnames),maxDataSet+1)
    default_data(:,:,i) = load(fnames(i).name);
  end


  m = mean(default_data,3); # get mean of data
			   # std deviation in each column of data
  m = m(:,1); # temp is col 1

  s = std(default_data,[],3);
  s = s(:,1);

  # std error
  se = s/sqrt(length(m));
  ts = tinv([0.025  0.975],length(m)-1); # t score
			    # calculate minimum confidence of column 1
  r = m + ts.*se;

  # check if data is in range
  con = default_data(:,1,:) > r(:,1) & default_data(:,1,:) < r(:,2);

  # get maximum of 2d truth table
  con = max(max(con));

endfunction
