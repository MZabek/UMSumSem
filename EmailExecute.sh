#!/bin/bash
# Bash script that is run periodically to update things... 

echo "Script run at:"
date
cd ~/Drive/admin/SummerSeminar2016/Code

# Calling updater script:
./UpdaterScript.sh >> ./UpdaterScript.log 

# Emails:
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' >> Emails.log
date >> Emails.log
python Emails.py >> Emails.log
