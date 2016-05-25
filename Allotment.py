# Program to set allotment of slots for summer seminar
# Mike Zabek
# Original: May 17, 2015

import sqlite3
import random
import re

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# Function to allocate people to the best of my ability
# Input: entry - list with: 
#           (In the following order) Timestamp,Username,SlotType,Availability
#       c   - cursor to SQLite database with TableName table
#       Allotted values go into "TableName" table of currently open SQL database...
#       Note SQL database must be open... 
def AllocatePerson(entry,c,TableName):
    #print "------------------------------Allocation call:------------------------------"
    # Checking section:
    #print "Checking: ",entry[1],"|",entry[0],"|Slot:",entry[2]
    Allotted = False
    c.execute('''CREATE TABLE IF NOT EXISTS %s (Timestamp text NOT NULL , Username text NOT NULL, SlotType text, Date text, CalDate text, Number int, PRIMARY KEY(Timestamp,Username))''' % (TableName))

    # First filling half slots:
    CurrPossDates = entry[3].split(", ")
    if entry[2] == "Half (40 minutes)":
        while Allotted == False and CurrPossDates:
            # Date selection algorythm:
            #Candidate:
            CheckDate =  random.choice(CurrPossDates) 

            # Checking if free half slot is acceptable:
            PreSelectedHalves = c.execute('''SELECT COUNT(Date),Date FROM %s WHERE Date = (?) AND SlotType = "Half (40 minutes)";''' % (TableName) , (CheckDate,))
            FreeHalfSlot = PreSelectedHalves.fetchall()
            if (1,CheckDate) in FreeHalfSlot:
                #print "Works: ",CheckDate
                AllocatedDate = CheckDate
                Allotted = True
                Number = 2
            else :
                #print "No slot: ",CheckDate
                CurrPossDates.remove(CheckDate)
                Allotted = False

    CurrPossDates = entry[3].split(", ")
    while Allotted == False and CurrPossDates:
        #Candidate:
        CheckDate =  random.choice(CurrPossDates) 
        # Checking if Checkdate works and allocating if it does:
        PreSelected =  c.execute('''SELECT Date,SlotType FROM %s WHERE Date = (?);'''%  (TableName), (CheckDate,))
        if not PreSelected.fetchall():
            #print "Works: ",CheckDate
            AllocatedDate = CheckDate
            Allotted = True
            Number = 1
        else:
            #print "Taken: ",CheckDate
            CurrPossDates.remove(CheckDate)

    # Inserting record of what happened into the database:
    if Allotted == True :
        # Modifying the dates to SQLite dates (CalDate):
        CalDate = re.sub("Monday |Wednesday |Friday ","2016-",AllocatedDate)
        CalDate = re.sub("May ","05-",CalDate)
        CalDate = re.sub("June ","06-",CalDate)
        CalDate = re.sub("July ","07-",CalDate)
        CalDate = re.sub("August ","08-",CalDate)
        CalDate = re.sub("September ","09-",CalDate)
        CalDate = re.sub("st$|th$|nd|rd$$","",CalDate)
        CalDate = re.sub(r'-(\d)$',r'-0\1',CalDate)

        c.execute('''INSERT INTO %s (Timestamp,Username,SlotType,Date,CalDate,Number) VALUES (?,?,?,?,?,?);''' % (TableName), (entry[0],entry[1],entry[2],AllocatedDate,CalDate,Number))




########################################
# Allotment call:

####################
#SQL Dataset connection:
sqlconn = sqlite3.connect('SumSemData.db')
c = sqlconn.cursor()
TempTable = 'TempAllotment'


# Random seed:
random.seed(20150599)
Iterations = 10000


iter = 1
MinLossFn = 10^6
while iter in range (1,Iterations) and MinLossFn > 0 :
    print "________________________________________________________________________________"
    print "Iteration: ",iter," of ",Iterations,"| Min:",MinLossFn
    # Cleaning up so fresh tables will be created:
    c.execute('''DROP TABLE IF EXISTS %s''' % TempTable)

    #########
    # Pull of list of entries, sorted by priority
    # First entry for each person:
    SignupPullEntry = c.execute('''SELECT Timestamp,Username,SlotType,Availability,JobTalk
                                        FROM Signup GROUP BY Username
                                        ORDER BY JobTalk DESC,  SlotType ASC, random();''')
    entries = SignupPullEntry.fetchall()
    # Then subsequent entries:
    SignupPullEntry = c.execute('''SELECT Timestamp,Username,SlotType,Availability,JobTalk 
                                        FROM Signup 
                                        WHERE Timestamp NOT IN (
                                            SELECT Timestamp
                                            FROM Signup
                                            GROUP BY Username
                                            ORDER BY JobTalk DESC, SlotType ASC, random());''')
    entries.extend(SignupPullEntry.fetchall())

    # Allocating based on the list:
    for entry in entries:
        AllocatePerson(entry,c,TempTable)

    # Showing results (Only in terms of people's first priority seminar): 
    # Note: The LossFn is haphazard --  Goes up with people not allocated any, with 1.01 weight to job candidates
    #                                   Then adds in 0.0001 if not putting in additional seminars...
    #                                   This is an inelegant way of putting in a hierarchical priority of things to accomplish
    #                                   It has not been optimized to avoid double counting
    Result =  c.execute('''SELECT Timestamp,Username,Signup.SlotType,CalDate,JobTalk,Availability FROM Signup 
                                        LEFT OUTER JOIN %s USING (Timestamp,Username) 
                                        GROUP BY Username
                                        ORDER BY JobTalk DESC,  Signup.SlotType ASC, random();''' % (TempTable))
    
    # Showing result and assigning loss fn:
    print "Allocation results:"

    NumJMPNotAssigned = 0
    NumPplNotAssigned = 0
    for entry in Result.fetchall() :
        if entry[3] == None :
            print "Username: ",entry[1],"|Slots allowed: ",entry[5].count(',')+1
            

            # Number of not assigned requests (maximizing number of slots used):
            NumPplNotAssigned = NumPplNotAssigned + 1
            # Tiebreaker for job market presentations:
            if entry[4] == 'Yes' :
                NumJMPNotAssigned = NumJMPNotAssigned + 1
    # Total slots not assigned
    NumReqNotAssigned = len(c.execute('''SELECT Timestamp 
                                        FROM Signup 
                                        LEFT OUTER JOIN %s USING (Timestamp,Username) 
                                        WHERE CalDate IS NULL;''' % (TempTable)).fetchall())

    # Final algorithm:
    LossFn = NumPplNotAssigned + 0.01*NumJMPNotAssigned + 0.0001*NumReqNotAssigned
    print "Loss function value: ",LossFn

    # Determining if this is the ``best'' allotment yet: 
    if LossFn < MinLossFn :
        # If so, setting as new benchmark
        MinLossFn = LossFn
        c.execute('''DROP TABLE IF EXISTS Allotment;''')
        c.execute('''ALTER TABLE %s RENAME TO Allotment;''' % (TempTable))
    c.execute('''DROP TABLE IF EXISTS %s;''' % (TempTable))

    # Iterating counter:
    iter = iter + 1

print "Minimum of loss function: ",MinLossFn

# Committing changes
sqlconn.commit()

print "--------------------------------------------------------------------------------"
print "Decided upon allocation:"
AllottedList = c.execute('''SELECT Username,Signup.SlotType,CalDate,JobTalk,Availability FROM Signup LEFT OUTER JOIN Allotment USING (Timestamp,Username) ORDER BY DATE(CalDate);''')
for Entry in AllottedList.fetchall() :
    print Entry[2],"Username: ",Entry[0],"Slots listed: ",Entry[4].count(',')+1


########################################
# Populating (first) schedule:
print "________________________________________________________________________________"
print "Making up first schedule:"

# This defines the table schema:
c.execute('''DROP TABLE IF EXISTS Schedule''')
c.execute('''CREATE TABLE Schedule (Date text NOT NULL, Number int DEFAULT 1, Title text, Presenter text, Abstract text, CoAuthors text, Room text DEFAULT 'Lorch 301', Comments text, Email text, SignupTime text, SlotType text, Scheduled text DEFAULT CURRENT_TIMESTAMP, CheckIn text, WebPost text, Misc text, Link text, PRIMARY KEY(Date,Number))''')


# Pulling entries
CalEntries = c.execute('''SELECT Allotment.CalDate,Allotment.Number,Signup.Title,Signup.Presenter,Signup.Abstract,Signup.CoAuthors,Username,Timestamp,Signup.SlotType FROM Allotment JOIN Signup USING (Timestamp,Username) ORDER BY CalDate ASC, Number ASC;''')
# Putting into schedule table:
for CalEntry in CalEntries.fetchall() :
    # Room entry, based on Olga's email (At a future date this should be stored externally) :
    if CalEntry[0].decode('UTF-8')=='2016-07-18' or CalEntry[0].decode('UTF-8')=='2016-07-20' or CalEntry[0].decode('UTF-8')=='2016-07-22' :
        Room = "Lorch 201"
    else :
        Room = "Lorch 301"

    # Inserting:
    c.execute('''INSERT INTO Schedule (Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SignupTime,SlotType,Room) VALUES (?,?,?,?,?,?,?,?,?,?);''', (CalEntry[0],CalEntry[1],CalEntry[2],CalEntry[3],CalEntry[4],CalEntry[5],CalEntry[6],CalEntry[7],CalEntry[8],Room))


print "Schedule completed, exiting"
print "________________________________________________________________________________"

# Committing changes to the database
sqlconn.commit()
# Closing connection
sqlconn.close()

