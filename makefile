# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

	
# The schedule: 
../Website/schedule.md MakeMDSchedule.log : SumSemData.db MakeMDSchedule.py 
	# Making schedule for website:
	python MakeMDSchedule.py > MakeMDSchedule.log
	# Posting to website
	cd ../Website
	bundle exec jekyll build
	git add --all
	git commit -m "Intitial allocation, $(DATE)"
	git push origin gh-pages

# The sign up and allotment: 
# Note: This should only be created once, at the official allotment date
# This was 6/22/2016 for the 2016 season
UpdateSignup.log Allotment.log ./archive/SumSemDataAtAllotment.db : UpdateSignup.py  Allotment.py ../Forms/SignupForm\ (Responses)\ -\ Form\ Responses\ 1.csv ../Forms/Email\ signup\ (Responses)\ -\ Form\ Responses\ 1.csv
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	cp SumSemData.db ./archive/SumSemDataAtAllotment.db
	# Making schedule for website:
	python MakeMDSchedule.py > MakeMDSchedule.log
	# Posting to website
	cd ../Website
	bundle exec jekyll build
	git add --all
	git commit -m "Intitial allocation, $(DATE)"
	git push origin gh-pages
	# At this point you write a nice email message to the people who were not allocated slots
	# And a general email message to everyone...

# Cleaning the directory
#.PHONY : clean
#clean : 
#	rm SumSemData.db
#	rm *.log
#
