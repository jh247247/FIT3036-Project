# use instead of temp to disable invasive
normal_name = 'normal';
invasive_opt = '-b';
script = fullfile(pwd,'sims.sh');
minRuns = 10

runsims = @(iter, temp, opt) system([script ' ' iter ' ' temp ' ' opt]);

# run normal first...

run = 0

while(confidence(normal_name) || run < minRuns)
     runsims(num2str(run),normal_name,'')
done

plotOutput(normal_name,inf);
