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

# Emails:
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' >> Emails.log
date >> Emails.log
python Emails.py >> Emails.log

# Updating the schedule on the website if there are any changes:
# As of May 29th this will always run because the dataset changes (trivially) with each update:
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' >> ScheduleUpdater.log
date >> ScheduleUpdater.log
make ../Website/schedule.md >> ScheduleUpdater.log

