#!/bin/bash
# Bash script that is run periodically to update things... 

cd ~/Drive/admin/SummerSeminar2016/Code

# Backing up dataset:
CURDATE=$(date +"%Y%m%d")
cp SumSemData.db ./archive/SumSemData$CURDATE.db

# Periodic updates and emails:
python UpdateSchedFromCheckIns.py >> UpdateSchedFromCheckIns.log
python Emails.py >> Emails.log

# Updating the schedule on the website if there are any changes:
# As of May 29th this will always run because the dataset changes (trivially) with each update:
make ../Website/schedule.md

