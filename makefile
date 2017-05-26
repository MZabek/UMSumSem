# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

	
# Update the website/schedule: 
# Note that git has to be configured here to work without a password 
# It will also ignore errors, since these will occur when there are no changes
# to the repository and commits/pushes occur... 
./WebsiteSetup/schedule.md MakeMDSchedule.log : ../Database/SumSemData.db MakeMDSchedule.py 
	# Making schedule for website:echo "Making schedule:"
	echo "Making schedule"
	date > MakeMDSchedule.log
	python MakeMDSchedule.py >> MakeMDSchedule.log

# The sign up and allotment: 
# Note: This should only be created once, at the official allotment date
# This was 6/22/2016 for the 2016 season
ProductionAllotment : UpdateSignup.py  Allotment.py ../Forms/2017\ SignupForm.csv ../Forms/2017\ Email\ signup.csv
	# Reading in from csv files:
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	mkdir ../archive/ || true
	cp ../Database/SumSemData.db ../archive/SumSemDataAtAllotment.db
	# Making schedule for website:
	python MakeMDSchedule.py > MakeMDSchedule.log

	# Building and posting website:
	cd WebsiteSetup; JEKYLL_ENV=production jekyll build 
	aws s3 sync WebsiteSetup/_site/ s3://seminar.mikezabek.com/
	# At this point you write a nice email message to the people who were not allocated slots
	# And a general email message to everyone...

TestAllotment : UpdateSignup.py  Allotment.py ../Forms/2017\ SignupForm.csv ../Forms/2017\ Email\ signup.csv
	# Reading in from csv files:
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	mkdir ../archive/ || true
	# Making schedule for website:
	python MakeMDSchedule.py > MakeMDSchedule.log

	# Building and posting website:
	cd WebsiteSetup; jekyll build 

# Cleaning the directory
#.PHONY : clean
#clean : 
#	rm SumSemData.db
#	rm *.log
#
