run_temps = 22.5:1:60.5;
                                # cell temp prefixes
prefixes = [{'normal'}; strread(num2str(run_temps),'%s')];

invasive_opt = '-b';
script = fullfile(pwd,'sims.sh');
minRuns = 10;
maxRuns = 30;
confidenceMax = 0.5;
data_length = 100001;
mean_tolerance = 0.5;

                           # anonymous function to make life easier...
runsims = @(iter, temp, opt) system([script ' ' iter ' ' temp ' ' opt]);

                         # keep track of the amount of runs per prefix
run = zeros([length(prefixes) 1]);

                          # keep track of all the confidence intervals
cons = zeros([length(prefixes),2,data_length]);

         # figure out which steps to ignore, since mean is too similar
keepSteps = @(p1,p2) abs(mean(p1) - \
                         mean(p2)) > mean_tolerance;

overlap = @(s1,s2) max(s1(:,1),s2(:,1)) - min(s1(:,2),s2(:,2)) < 0;

keepRunning = ones([length(prefixes), 1]);

while max(keepRunning) == 1
  run
  for i = 1:length(prefixes)
    if keepRunning(i) == 1
      if(i == 1) # normal case
        runsims(num2str(run(i)),char(prefixes(i)),'');
      else # invasive black
        runsims(num2str(run(i)),char(prefixes(i)),'-b');
      end
      if run(i) < minRuns
        run(i) = run(i) + 1
        continue
      end
                                # set confidence interval
      cons(i,:,:) = confidence(char(prefixes(i)),run(i))';

            # find out if we still need to keep running this iteration
# assumes that once an iteration stops, it really does not ever run again
      if i == 1
                 # compare overlaps with adjacent samples
                 # ignore parts that confidence interval is very small
        keep = keepSteps(cons(i,:,:),cons(i+1,:,:));
        if all(keep == 0)
          keepRunning(i) = 0;
          continue
        end
        o = overlap(cons(i,:,keep), cons(i+1,:,keep));
      elseif i == length(prefixes)
        keep = keepSteps(cons(i,:,:),cons(i-1,:,:));
        if all(keep==0)
          keepRunning(i) = 0;
          continue
        end
        o = overlap(cons(i,:,keep), cons(i-1,:,keep));
      else
        keep = keepSteps(cons(i,:,:),cons(i-1,:,:)) | keepSteps(cons(i,:,:),cons(i+1,:,:));
        if all(keep==0)
          keepRunning(i) = 0;
          continue
        end
        o = overlap(cons(i,:,keep), cons(i-1,:,keep)) | overlap(cons(i,:,keep), cons(i+1,:,keep));
      end

      keepRunning(i) = max(o) & run(i) < maxRuns | run(i) < minRuns
      run(i) = run(i) + 1
    end
  end
end

for i = 1:length(prefixes)
  plotOutput(char(prefixes(i)),run(i));
end
