# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

# The sign up and allotment: 
UpdateSignup.log Allotment.log ./archive/SumSemDataAtAllotment.db : UpdateSignup.py  Allotment.py ../Forms/SignupForm\ (Responses)\ -\ Form\ Responses\ 1.csv ../Forms/Email\ signup\ (Responses)\ -\ Form\ Responses\ 1.csv
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	cp SumSemData.db ./archive/SumSemDataAtAllotment.db
	
# The schedule: 
../Website/schedule.md MakeMDSchedule.log : SumSemData.db MakeMDSchedule.py 
	python MakeMDSchedule.py > MakeMDSchedule.log

# Cleaning the directory
#.PHONY : clean
#clean : 
#	rm SumSemData.db
#	rm *.log
#
