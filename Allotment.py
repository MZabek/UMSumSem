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
#       c   - cursor to SQLite database with Allotment table
#       Allotted values go into "Allotment" table of currently open SQL database...
#       Note SQL database must be open... 
def AllocatePerson(entry,c):
    print "------------------------------Allocation call:------------------------------"
    # Checking section:
    print "Checking: ",entry[1],"|",entry[0],"|Slot:",entry[2]
    Allotted = False
    c.execute('''CREATE TABLE IF NOT EXISTS Allotment (Timestamp text PRIMARY KEY, Username text, SlotType text, Date text, CalDate text, Number int)''')
    c.execute('''CREATE TABLE IF NOT EXISTS WasAllotted (Timestamp text PRIMARY KEY, Username text, SlotType text, Allotted int)''')

    # First filling half slots:
    CurrPossDates = entry[3].split(", ")
    if entry[2] == "Half (40 minutes)":
        while Allotted == False and CurrPossDates:
            # Date selection algorythm:
            #Candidate:
            CheckDate =  random.choice(CurrPossDates) 
            print "Checking for previous half slot on: ",CheckDate

            # Checking if free half slot is acceptable:
            PreSelectedHalves = c.execute('''SELECT COUNT(Date),Date FROM Allotment WHERE Date = (?) AND SlotType = "Half (40 minutes)";''', (CheckDate,))
            FreeHalfSlot = PreSelectedHalves.fetchall()
            if (1,CheckDate) in FreeHalfSlot:
                print "Half slot available: ",FreeHalfSlot
                AllocatedDate = CheckDate
                Allotted = True
                Number = 2
            else :
                print "No half slot fitting"
                CurrPossDates.remove(CheckDate)
                Allotted = False

    CurrPossDates = entry[3].split(", ")
    while Allotted == False and CurrPossDates:
        #print "------------------------------------------------------------"
        #print "Dates to check: ", CurrPossDates
        #Candidate:
        CheckDate =  random.choice(CurrPossDates) 
        print "Checking: ",CheckDate
        # Checking if Checkdate works and allocating if it does:
        PreSelected =  c.execute('''SELECT Date,SlotType FROM Allotment WHERE Date = (?);''', (CheckDate,))
        if not PreSelected.fetchall():
            print "This is empty, filling it"
            AllocatedDate = CheckDate
            Allotted = True
            Number = 1
        else:
            print "This has something in it already"
            CurrPossDates.remove(CheckDate)
            #print "Possible dates: ",CurrPossDates

    # Inserting record of what happened into the database:
    c.execute('''INSERT INTO WasAllotted (Timestamp,Username,SlotType,Allotted) 
                VALUES (?,?,?,?);''', (entry[0],entry[1],entry[2],Allotted))
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

        c.execute('''INSERT INTO Allotment (Timestamp,Username,SlotType,Date,CalDate,Number) VALUES (?,?,?,?,?,?);''', (entry[0],entry[1],entry[2],AllocatedDate,CalDate,Number))




#####
# Allotment call:

# Random seed:
random.seed(20150599)

#SQL Dataset connection:
sqlconn = sqlite3.connect('SumSemData.db')
c = sqlconn.cursor()

# Cleaning up so fresh tables will be created:
c.execute('''DROP TABLE IF EXISTS Allotment''')
c.execute('''DROP TABLE IF EXISTS WasAllotted''')

# Pull of list of entries, sorted by priority (right now not really putting in a very sophisticated priority ranking)
SignupPull =  c.execute('''SELECT Timestamp,Username,SlotType,Availability FROM Signup WHERE Username <> "" ORDER BY JobTalk DESC, SlotType ASC, random();''')
entries = SignupPull.fetchall()

for entry in entries:
    AllocatePerson(entry,c)

print "________________________________________________________________________________"
print "Allocation results:"
print "Timestamp, Username, SlotType, Allotted"
WasAllotted = c.execute('''SELECT * FROM WasAllotted;''')
for Entry in WasAllotted.fetchall():
    print Entry

# Committing changes
sqlconn.commit()
# Closing connection
sqlconn.close()

