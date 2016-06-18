#!/bin/bash
# Bash script that is run periodically to update things... 

echo "Script run at:"
date


cd ~/Drive/admin/SummerSeminar2016/Code

# Backing up database:
CURDATE=$(date +"%Y%m%d")
cp SumSemData.db ./archive/SumSemData$CURDATE.db

# Periodic updates:
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' >> UpdateSchedFromCheckIns.log
date >> UpdateSchedFromCheckIns.log
python UpdateSchedFromCheckIns.py >> UpdateSchedFromCheckIns.log

# Updating the schedule on the website if there are any changes
# Note: some may not be relevant to the website
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' >> ScheduleUpdater.log
date >> ScheduleUpdater.log
python MakeMDSchedule.py >> ScheduleUpdater.log

# Posting to website
cd ../Website/ >> ~/Drive/admin/SummerSeminar2016/Code/ScheduleUpdater.log
bundle exec jekyll build >> ~/Drive/admin/SummerSeminar2016/Code/ScheduleUpdater.log

# Putting all into git tracking:
git add --all >> ~/Drive/admin/SummerSeminar2016/Code/ScheduleUpdater.log
# If a change commiting and pushing it up:
if ! git diff-index --quiet HEAD --; then
  git commit -m "Automatic schedule update" >> ~/Drive/admin/SummerSeminar2016/Code/ScheduleUpdater.log
  git push origin gh-pages >> ~/Drive/admin/SummerSeminar2016/Code/ScheduleUpdater.log  
fi

