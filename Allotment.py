# Program to set allotment of slots for summer seminar
# Mike Zabek
# Original: May 17, 2015

import sqlite3
import random
import re
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# Function to allocate people, based on current listing of allocations 
#       Algorithm - If half, put in first available half slot on list, then make half slot from list
#                 - If fill, put in first available full slot in the list  
# Input: entry - list with: 
#           (In the following order) SignupID,SlotType,Availability
#       c   - cursor to SQLite database with TableName table
#       Allotted values go into "TableName" table of currently open SQL database...
#       Note SQL database must be open... 
# Output: This will potentially modify the dataset in s by putting in the value
def AllocatePerson(entry,c,TableName):
    #print "------------------------------Allocation call:------------------------------"
    # Checking section:
    #print "Checking: ",entry[0],"|",entry[1],"|Slots:",entry[2]
    Allotted = False
    # NOTE: Date is date from signup, Caldate is formatted so it is easier to work with in SQL/python
    c.execute('''CREATE TABLE IF NOT EXISTS %s (SignupID INTEGER, SlotType text, Date text, Number int, CalDate text, PRIMARY KEY(Date, Number))''' % (TableName))

    # Listing of dates to check in order for half then full
    CurrPossDates = entry[2]
    ## checking each possible date, in order to see if there is a half slot avaiable
    if entry[1] == "Half (40 minutes)":
        date_checked = 0
        while Allotted == False and date_checked < len(CurrPossDates) :
            # Taking out the first date in the remaining list:
            check_date = CurrPossDates[date_checked]

            # Checking if free half slot is acceptable:
            PreSelectedHalves = c.execute('''SELECT COUNT(Date),Date FROM %s WHERE Date = (?) AND SlotType = "Half (40 minutes)";''' % (TableName) , (check_date,))
            FreeHalfSlot = PreSelectedHalves.fetchall()
            if (1,check_date) in FreeHalfSlot:
                #print "Works with pre-existing half: ",check_date
                AllocatedDate = check_date
                Allotted = True
                Number = 2
            else :
                #print "No pre-existing half slot: ",check_date
                Allotted = False
            date_checked = date_checked + 1

    ## Assinging an avaiable full slot if full, or no half slot already assigned
    while Allotted == False and len(CurrPossDates) > 0 :
        # Taking out the first date in the remaining list:
        check_date = CurrPossDates.pop(0)
        # Checking if check_date works and allocating if it does:
        PreSelected =  c.execute('''SELECT Date,SlotType FROM %s WHERE Date = (?);'''%  (TableName), (check_date,))
        if not PreSelected.fetchall():
            #print "Works with full: ",check_date
            AllocatedDate = check_date
            Allotted = True
            Number = 1
        else:
            #print "Taken full slot: ",check_date
            Allotted = False

    # Inserting record of what happened into the database:
    if Allotted == True :
        # Modifying the dates to SQLite dates (CalDate):
        CalDate = re.sub("Monday, |Wednesday, |Friday, ","2017-",AllocatedDate)
        CalDate = re.sub("May ","05-",CalDate)
        CalDate = re.sub("June ","06-",CalDate)
        CalDate = re.sub("July ","07-",CalDate)
        CalDate = re.sub("August ","08-",CalDate)
        CalDate = re.sub("September ","09-",CalDate)
        CalDate = re.sub("st$|th$|nd|rd$$","",CalDate)
        CalDate = re.sub(r'-(\d)$',r'-0\1',CalDate)

        c.execute('''INSERT INTO %s (SignupID,Date,SlotType,Number,CalDate) VALUES (?,?,?,?,?);''' % (TableName), (entry[0],AllocatedDate,entry[1],Number,CalDate))




########################################
# Allotment call:

####################
#SQL Dataset connection:
sqlconn = sqlite3.connect('../Database/SumSemData.db')
c = sqlconn.cursor()


# Random seed:
random.seed(20150599)
Iterations = 1


iter = 1
MinLossFn = 10^6
while iter in range (1,Iterations+1) and MinLossFn > -1 :
    print "________________________________________________________________________________"
    print "Iteration: ",iter," of ",Iterations,"| Min:",MinLossFn
    # Cleaning up so fresh tables will be created:
    c.execute('''DROP TABLE IF EXISTS TempAllotment''')

    #########
    # Pull of list of entries, sorted by priority
    # First entry for each person:
    SignupPull = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk
                                        FROM Signup
                                        ORDER BY JobTalk DESC,  SlotType ASC, random();''')
    SignupList = SignupPull.fetchall()

    # Allocating based on the list:
    for entry in SignupList:

        ## Making the workable dates into a list:
        # Note: Here a date is just a unique string... 
        # And I have a really inellegant way of taking out empty strings
        preferred_datel = entry[2].split(";")
        while '' in preferred_datel:
            preferred_datel.remove('')
        random.shuffle(preferred_datel)

        workable_datel = entry[3].split(";")
        while '' in workable_datel:
            workable_datel.remove('')
        random.shuffle(workable_datel)
        
        available_dates = preferred_datel + workable_datel
        #print entry
        #print available_dates 

        # Caling AllocatePerson 
        AllocatePerson((entry[0],entry[1],available_dates),c,'TempAllotment')

    ########################################
    # Showing result and assigning loss fn:
    # Note: The LossFn is haphazard --  Goes up with people not allocated any, with 1.01 weight to job candidates
    #                                   Then adds in 0.0001 if not putting in additional seminars...
    #                                   This is an inelegant 
    #                                   It has not been optimized to avoid double counting
    print "Allocation results:"

    Result =  c.execute('''SELECT Signup.Username,Signup.SlotType,Date,Signup.JobTalk,PreferredDates,WorkableDates FROM Signup 
                                        LEFT OUTER JOIN TempAllotment USING (SignupID) 
                                        GROUP BY Username
                                        ORDER BY Signup.JobTalk DESC,  Signup.SlotType ASC, random();''')
    NumJMPNotAssigned = 0
    NumPplNotAssigned = 0
    for entry in Result.fetchall() :
        if entry[3] == None :
            print "Not assigned username: ",entry[1],"|Slots allowed: ",entry[5].count(',')+1

            # Number of not assigned requests (maximizing number of slots used):
            NumPplNotAssigned = NumPplNotAssigned + 1
            # Tiebreaker for job market presentations:
            if entry[4] == 'Yes' :
                NumJMPNotAssigned = NumJMPNotAssigned + 1

    # Total slots not assigned
    NumReqNotAssigned = len(c.execute('''SELECT Username 
                                        FROM Signup 
                                        LEFT OUTER JOIN TempAllotment USING (SignupID) 
                                        WHERE TempAllotment.Date IS NULL;''').fetchall())

    # Final algorithm:
    LossFn = NumPplNotAssigned + 0.01*NumJMPNotAssigned + 0.0001*NumReqNotAssigned
    print "Loss function value: ",LossFn

    # Determining if this is the ``best'' allotment yet: 
    if LossFn < MinLossFn :
        # If so, setting as new benchmark
        MinLossFn = LossFn
        c.execute('''DROP TABLE IF EXISTS Allotment;''')
        c.execute('''ALTER TABLE TempAllotment RENAME TO Allotment;''')
    c.execute('''DROP TABLE IF EXISTS TempAllotment;''')

    # Iterating counter:
    iter = iter + 1

########################################
# Done with allocation
print "Minimum of loss function: ",MinLossFn

# Committing changes
sqlconn.commit()

print "--------------------------------------------------------------------------------"
print "Decided upon allocation:"
AllottedList = c.execute('''SELECT Username,JobTalk,Date FROM Signup LEFT OUTER JOIN Allotment USING (SignupID) ORDER BY CalDate;''')
for Entry in AllottedList.fetchall() :
    print Entry[2],"Username: ",Entry[0],"Job talk: ",Entry[1]


########################################
# Populating (first) schedule:
print "________________________________________________________________________________"
print "Making up first schedule:"

# MODIFY: This defines the table schema:
c.execute('''DROP TABLE IF EXISTS Schedule''')
c.execute('''
        CREATE TABLE Schedule 
        (ScheduleID INTEGER PRIMARY KEY  AUTOINCREMENT, 
        Date text NOT NULL, Number int DEFAULT 1, Email text NOT NULL, Title text, 
        Presenter text, Abstract text, CoAuthors text, Notes text, 
        SlotType text DEFAULT "Standard (80 minutes)", SignupTime text, 
        Scheduled text DEFAULT CURRENT_TIMESTAMP, 
        CheckInDate text, AnnouncementDate text, CancellationDate text, Link text,  
        LastEmail text)''')

# Pulling Signup data to populate calendar
c.execute('''
        INSERT INTO Schedule (ScheduleID,Date,Number,Email,Title,Presenter,CoAuthors,Abstract,SlotType)
        SELECT Signup.SignupID,Allotment.CalDate,Allotment.Number,Signup.Username,Signup.Title,Signup.Presenter,Signup.CoAuthors,Signup.Abstract,Signup.SlotType 
        FROM Allotment JOIN Signup USING (SignupID) 
        ORDER BY Allotment.CalDate ASC, Allotment.Number ASC;
        ''')



print "Schedule completed, exiting"
print "________________________________________________________________________________"

# Committing changes to the database
sqlconn.commit()
# Closing connection
sqlconn.close()

