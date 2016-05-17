# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

# The sign up and allotment: 
SumSemData.db UpdateSignup.log Allotment.log : UpdateSignup.py  Allotment.py ../Forms/SignupForm\ (Responses)\ -\ Form\ Responses\ 1.csv ../Forms/Email\ signup\ (Responses)\ -\ Form\ Responses\ 1.csv
	python UpdateSignup.py > UpdateSignup.log
	python Allotment.py > Allotment.log
	
# The schedule: 
../Website/schedule.md MakeMDSchedule.log : SumSemData.db MakeMDSchedule.py 
	python MakeMDSchedule.py > MakeMDSchedule.log

# Cleaning the directory
.PHONY : clean
clean : 
	rm SumSemData.db
	rm *.log

