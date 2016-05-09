# build the presentation, including moving files to where they should be



# Main setup
#.PHONY : all
#all : Zabek16LabLunch.pdf 

# Updating the sign up stuff: 
SumSemData.db : UpdateSignup.py ../Forms/SignUpForm.csv
	python UpdateSignup.py >> UpdateSignup.log
	
	
# Cleaning the directory
.PHONY : clean
clean : 
	rm SumSemData.db

