# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

	
# Update the website/schedule: 
# Note that git has to be configured here to work without a password 
# It will also ignore errors, since these will occur when there are no changes
# to the repository and commits/pushes occur... 
../Website/schedule.md MakeMDSchedule.log : SumSemData.db MakeMDSchedule.py 
	# Making schedule for website:echo "Making schedule:"
	echo "Making schedule"
	date > MakeMDSchedule.log
	python MakeMDSchedule.py >> MakeMDSchedule.log

# The sign up and allotment: 
# Note: This should only be created once, at the official allotment date
# This was 6/22/2016 for the 2016 season
UpdateSignup.log Allotment.log ./archive/SumSemDataAtAllotment.db : UpdateSignup.py  Allotment.py ../Forms/2017\ SignupForm.csv ../Forms/2017\ Email\ signup.csv
	# Reading in from csv files:
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	cp SumSemData.db ./archive/SumSemDataAtAllotment.db
	# Making schedule for website:
	python MakeMDSchedule.py > MakeMDSchedule.log
	# Posting to website
	BUNDLE_GEMFILE=../Website/Gemfile bundle exec jekyll build
	rm -r _site/
	GIT_DIR=../Website/.git GIT_WORK_TREE=../Website git add --all
	GIT_DIR=../Website/.git GIT_WORK_TREE=../Website git commit -m "Intitial allocation"
	GIT_DIR=../Website/.git GIT_WORK_TREE=../Website git push origin gh-pages
	# At this point you write a nice email message to the people who were not allocated slots
	# And a general email message to everyone...

# Cleaning the directory
#.PHONY : clean
#clean : 
#	rm SumSemData.db
#	rm *.log
#
