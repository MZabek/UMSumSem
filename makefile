# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all

# Updating the sign up stuff: 
SumSemData.db UpdateSignup.log : UpdateSignup.py ../Forms/SignupForm\ (Responses)\ -\ Form\ Responses\ 1.csv ../Forms/Email\ signup\ (Responses)\ -\ Form\ Responses\ 1.csv
	python UpdateSignup.py >> UpdateSignup.log
	
	
# Cleaning the directory
.PHONY : clean
clean : 
	rm SumSemData.db

