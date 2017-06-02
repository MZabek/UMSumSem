# Program to set allotment of slots for summer seminar
# Mike Zabek
# Original: May 17, 2015

import sqlite3
import regex as re
import random
import sys
import codecs
from kitchen.text.converters import getwriter

# Suggested fix for printing unicode strings in terminal...
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


########################################
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
    if entry[1] == u'Half (40 minutes)':
        date_checked = 0
        while Allotted == False and date_checked < len(CurrPossDates) :
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

        # Checking types are as expected:
        assert type(entry[0]) == int;
        assert type(AllocatedDate) == unicode;
        assert type(entry[1]) == unicode;
        assert type(Number) == int;
        assert type(CalDate) == unicode;

        c.execute('''INSERT INTO %s (SignupID,Date,SlotType,Number,CalDate) VALUES (?,?,?,?,?);''' % (TableName), (entry[0],AllocatedDate,entry[1],Number,CalDate))




########################################
# Allotment call:

####################
#SQL Dataset connection:
sqlconn = sqlite3.connect('../Database/SumSemData.db')
sqlconn.text_factory = unicode
c = sqlconn.cursor()


# Random seed:
random.seed(20150599)
Iterations = 10000


iter = 1
# TODO: This could be parallelized
MinLossFn = 10^6
MaxStartDate = u'1900-01-01'
while iter in range (1,Iterations+1) and MinLossFn > 0 :
    print "________________________________________________________________________________"
    print "Iteration: ",iter," of ",Iterations,"| Min loss fn:",MinLossFn,"| Max start date: ",MaxStartDate
    # Cleaning up so fresh tables will be created:
    c.execute('''DROP TABLE IF EXISTS TempAllotment''')

    #########
    # Pull of list of entries, sorted by priority
    # TODO: May be better to assign a priority field to people, and could simplify evaluating
    #       how well the allotment process did
    
    ## Creating cursors to pulls of each group:
    # Job talk people with only one entry
    OneJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk
                                FROM Signup GROUP BY Username 
                                HAVING COUNT(SignupID) = 1 AND JobTalk = "Yes";''').fetchall()
    # Not job talk people with only one entry
    OneNJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk 
                                FROM Signup GROUP BY Username 
                                HAVING COUNT(SignupID) = 1 AND JobTalk = "No";''').fetchall()

    # People with two entries and job talk, taking Job talk:
    FirstWTwoJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk 
                                FROM Signup 
                                WHERE Username IN 
                                    (SELECT Username 
                                        FROM Signup GROUP BY Username 
                                        HAVING COUNT(SignupID) >= 2 
                                        AND MAX(JobTalk) = "Yes") 
                                    AND JobTalk = "Yes";''').fetchall()
    FirstWTwoNoJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk 
                                    FROM Signup 
                                    WHERE SignupID 
                                    IN (SELECT MIN(SignupID) FROM Signup 
                                            WHERE Username IN 
                                            (SELECT Username FROM Signup GROUP BY Username 
                                            HAVING COUNT(SignupID) >= 2 
                                            AND MAX(JobTalk) = "No") 
                                        GROUP BY Username);''').fetchall() 
    # Remaining entries for people
    SecondWTwoJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk 
                                FROM Signup 
                                WHERE Username IN 
                                    (SELECT Username 
                                        FROM Signup GROUP BY Username 
                                        HAVING COUNT(SignupID) >= 2 
                                        AND MAX(JobTalk) = "Yes") 
                                    AND NOT JobTalk = "Yes";''').fetchall()
    SecondWTwoNoJMPSignup = c.execute('''SELECT SignupID,SlotType,PreferredDates,WorkableDates,JobTalk 
                                    FROM Signup 
                                    WHERE SignupID NOT IN 
                                            (SELECT MIN(SignupID) FROM Signup 
                                            WHERE Username IN 
                                                (SELECT Username FROM Signup GROUP BY Username 
                                                HAVING COUNT(SignupID) >= 2 
                                                AND MAX(JobTalk) = "No") 
                                            GROUP BY Username)
                                        AND Username IN 
                                            (SELECT Username FROM Signup GROUP BY Username 
                                            HAVING COUNT(SignupID) >= 2 
                                            AND MAX(JobTalk) = "No")
                                         ;''').fetchall()
    # Priority lists
    TopPriority = OneJMPSignup + FirstWTwoJMPSignup
    MiddlePriority = OneNJMPSignup + FirstWTwoNoJMPSignup
    BottomPriority = SecondWTwoJMPSignup + SecondWTwoNoJMPSignup

    # Randomizing each and putting together
    random.shuffle(TopPriority)
    random.shuffle(MiddlePriority)
    random.shuffle(BottomPriority)
    SignupList = TopPriority + MiddlePriority + BottomPriority

    # Allocating based on the list:
    # TODO: It would probably be (a lot) faster to do all of this is memory 
    #       as opposed to writing to disk
    for to_assign in SignupList:

        ## Making the workable dates into a list:
        # Note: Here a date is just a unique string... 
        # And I have a really inellegant way of taking out empty strings
        preferred_datel = to_assign[2].split(";")
        while '' in preferred_datel:
            preferred_datel.remove('')
        random.shuffle(preferred_datel)

        workable_datel = to_assign[3].split(";")
        while '' in workable_datel:
            workable_datel.remove('')
        random.shuffle(workable_datel)
        
        available_dates = preferred_datel + workable_datel
        #print to_assign
        #print available_dates 

        # Caling AllocatePerson 

        # Ensuring I made everything unicode:
        assert type(to_assign[0]) == int
        assert type(to_assign[1]) == unicode
        for date in available_dates :
            assert type(date) == unicode
        AllocatePerson((to_assign[0],to_assign[1],available_dates),c,'TempAllotment')

    ########################################
    # Shwing result and assigning loss fn:
    # Note: The LossFn is haphazard --  Goes up with people not allocated any, with 1.01 weight to job candidates
    #                                   Then adds in 0.0001 if not putting in additional seminars...
    #                                   This is an inelegant 
    #                                   It has not been optimized to avoid double counting
    print "Allocation results:"

    ResultByPerson =  c.execute('''SELECT Username,MAX(Date),MAX(JobTalk) FROM Signup 
                                        LEFT OUTER JOIN TempAllotment USING (SignupID) 
                                        GROUP BY Username;''')
    NumJMPNotAssigned = 0
    NumPplNotAssigned = 0
    for entry in ResultByPerson.fetchall() :
        if entry[1] == None :
            print "Not assigned username: ",entry[0],"| Jobtalk? ",entry[2]

            # Number of not assigned people:
            NumPplNotAssigned = NumPplNotAssigned + 1
            # Tiebreaker for job market presentations:
            if entry[2] == 'Yes' :
                NumJMPNotAssigned = NumJMPNotAssigned + 1

    # Total slots not assigned
    ReqNotAssigned = c.execute('''SELECT Username,SignupID 
                                        FROM Signup 
                                        LEFT OUTER JOIN TempAllotment USING (SignupID) 
                                        WHERE Date IS NULL;''').fetchall()
    NumReqNotAssigned = len(ReqNotAssigned)

    StartDate = c.execute('''SELECT MIN(CalDate) FROM TempAllotment;''').fetchone()[0]
    # How to caompare the quality of an allocation:
    LossFn = NumPplNotAssigned + NumJMPNotAssigned + 0.0001*NumReqNotAssigned
    print "Start date: ",StartDate 
    print "Job market talks not assigned: ",NumJMPNotAssigned
    print "Total people not assigned: ",NumPplNotAssigned
    print "Requests not assigned: ",ReqNotAssigned
    print "Loss function value: ",LossFn

    # Determining if this is the ``best'' allotment yet:
    if LossFn < MinLossFn or (LossFn <= MinLossFn and StartDate > MaxStartDate) :
        # If so, setting as new benchmark
        MinLossFn = LossFn
        MaxStartDate = StartDate
        c.execute('''DROP TABLE IF EXISTS Allotment;''')
        c.execute('''ALTER TABLE TempAllotment RENAME TO Allotment;''')
    c.execute('''DROP TABLE IF EXISTS TempAllotment;''')

    # Iterating counter:
    iter = iter + 1

########################################
# Done with allocation
print "--------------------------------------------------------------------------------"
print "Finished searching for allocations"
print "Minimum of loss function: ",MinLossFn
print "Decided upon allocation:"

# Committing changes
sqlconn.commit()

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

