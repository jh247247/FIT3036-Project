# use instead of temp to disable invasive
normal_name = 'normal';
invasive_opt = '-b';
script = fullfile(pwd,'sims.sh');

runsims = @(iter, temp, opt) system([script ' ' iter ' ' temp ' ' opt]);

# run normal first...

runsims('0',normal_name,'')
runsims('4',normal_name,'')
runsims('8',normal_name,'')
runsims('12',normal_name,'')
plotOutput(normal_name,inf);
