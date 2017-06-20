# Program to create markdown schedule from SQLite schedule table
# Mike Zabek
# Original: May 17, 2016
# Takes the SumSemData.db Scheudle table and creates: 
#   ./WebsiteSetup/schedule.md and ./WebsiteSetup/_texts/____.md
#   These are things that will be on the website

import regex as re
import sqlite3
import sys
import os
import codecs
from kitchen.text.converters import getwriter

# Suggested fix for printing unicode strings in terminal...
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


########################################
#SQL Database connection:
sqlconn = sqlite3.connect('../Database/SumSemData.db')
# Testing
#sqlconn = sqlite3.connect('../Database/Testing/17AllotmentSumSemData.db')
c = sqlconn.cursor()

# Making folders for website:
if not os.path.exists('./WebsiteSetup/'):
    os.makedirs('./WebsiteSetup/')
if not os.path.exists('./WebsiteSetup/_posts/'):
    os.makedirs('./WebsiteSetup/_posts/')


################################################################################
# Full schedule:

# Opening
MDSchedule = codecs.open('./WebsiteSetup/schedule.md','w','utf-8')
MDSchedule.write('---\n')
MDSchedule.write('layout: page\n')
MDSchedule.write('title: Full schedule\n')
MDSchedule.write('---\n')

# Getting entries from database
print "Making full schedule with the following dates:"
CalEntries = c.execute('''SELECT Date,Number,Presenter,Title,CoAuthors,Abstract,SlotType,Link 
                            FROM Schedule ORDER BY Date ASC, Number ASC;''')
for CalEntry in CalEntries.fetchall() :

    # Getting room number, if in reservation section
    RoomList = c.execute('''SELECT Room 
                                FROM RoomReservations WHERE Date=?;''',
                                (CalEntry[0],)).fetchall()
    if RoomList :
        print RoomList[0]
        Room = RoomList[0][0]
    else :
        Room = None

    # Checking that stuff is unicode, integer, or empty:
    for info in CalEntry :
        assert (type(info) == unicode ) | (type(info) == int) | (info == None)

    #Stripping out year from date:
    Date = re.sub("20[12][0-9]-","",CalEntry[0])
    # Re-inserting months: 
    Date = re.sub("05-","May ",Date)
    Date = re.sub("06-","June ",Date)
    Date = re.sub("07-","July ",Date)
    Date = re.sub("08-","August ",Date)
    Date = re.sub("09-","September ",Date)
    print Date
    assert type(Date) == unicode

    # Writing text to file:
    # Date
    MDSchedule.write('## ')
    MDSchedule.write(Date)
    # Slot, if needed
    if CalEntry[6] and CalEntry[6] == 'Half (40 minutes)' :
        MDSchedule.write(' (Slot ')
        MDSchedule.write(str(CalEntry[1]))
        MDSchedule.write(')')
    # Presenter
    MDSchedule.write(' - ')
    MDSchedule.write(CalEntry[2])
    # Title
    if CalEntry[3] and CalEntry[3] != 'TBD' :
        MDSchedule.write('\n\n### ')
        MDSchedule.write(CalEntry[3])
    # Room, if specified
    if Room and Room != '' :
        MDSchedule.write('\n\n')
        MDSchedule.write('#### ')
        MDSchedule.write(Room)
    # Co Authors
    if CalEntry[4] and CalEntry[4] != '' and CalEntry[4] != 'N/A' and CalEntry[4] != None :
        MDSchedule.write('\n\n')
        MDSchedule.write('*Joint work with:* ')
        MDSchedule.write(CalEntry[4])
    # Abstract
    if CalEntry[5] and CalEntry[5] != 'TBD' :
        MDSchedule.write('\n\n')
        MDSchedule.write(CalEntry[5])
    # Link
    if CalEntry[7] and CalEntry[7] != 'TBD' :
        MDSchedule.write('\n\n')
        MDSchedule.write('[More information]('+CalEntry[8]+')')
    MDSchedule.write('\n\n')

# Closing and saving:
MDSchedule.close()

################################################################################
# Specific entries for upcoming events

# Getting entries

CalEntries = c.execute('''SELECT Date,Number,Presenter,Title,CoAuthors,Abstract,SlotType,Link 
                        FROM Schedule 
                        WHERE date(Date) >= date('now','-13 hours') 
                            AND date(Date) <= date('now','+120 days','-13 hours') 
                        ORDER BY date(Date) ASC, Number ASC;''')
TargetDir = u'./WebsiteSetup/_posts/'

# Removing all files in the directory:
print "Removing the following files:"
filelist = [ f for f in os.listdir(TargetDir) if f.endswith(".md") ]
for f in filelist:
    FullFile = TargetDir + f
    print FullFile
    os.remove(FullFile)

print "Creating the following files: "
for CalEntry in CalEntries.fetchall() :
    
    # Checking that stuff is unicode, integer, or empty:
    for info in CalEntry :
        assert (type(info) == unicode ) | (type(info) == int) | (info == None)

    # Getting room number, if in reservation section
    RoomList = c.execute('''SELECT Room 
                                FROM RoomReservations WHERE Date=?;''',
                                (CalEntry[0],)).fetchall()
    if RoomList :
        print RoomList[0]
        Room = RoomList[0][0]
    else :
        Room = None


    # Filename to save as: 
    # Date and presenter
    print TargetDir
    SaveAs = TargetDir
    SaveAs +=CalEntry[0]
    SaveAs +='-'
    Name = CalEntry[2].replace(' ','-')
    SaveAs +=Name
    SaveAs +='.md'
    # Outpiut of save is unicode
    assert type(SaveAs) == unicode
    print SaveAs


    #Stripping out year from date:
    Date = re.sub("2017-","",CalEntry[0])
    # Re-inserting months: 
    Date = re.sub("05-","May ",Date)
    Date = re.sub("06-","June ",Date)
    Date = re.sub("07-","July ",Date)
    Date = re.sub("08-","August ",Date)
    Date = re.sub("09-","September ",Date)

    # Title of the page: 
    Title = CalEntry[2]
    if CalEntry[3] and CalEntry[3] != 'TBD' and CalEntry[3] != 'title tk' and CalEntry[3] != 'Presentation TBD' and CalEntry[3] != 'My JMP (title under revision)':
        Title = Title + " - " + re.sub(":"," -",CalEntry[3])

    # Opening and writing header:
    MDEntry = codecs.open(SaveAs,'w','utf-8')
    MDEntry.write('---\n')
    MDEntry.write('layout: post\n')
    MDEntry.write('title: ')
    MDEntry.write(Title)
    MDEntry.write('\n')

    MDEntry.write('---\n')

    # Writing text to file:
    # Room number
    if Room and Room != '':
        MDEntry.write('#### ')
        MDEntry.write(Room)
    # Slot, if needed
    if CalEntry[6] and CalEntry[6] == 'Half (40 minutes)' :
        MDEntry.write('\n\n')
        MDEntry.write('#### (Slot ')
        MDEntry.write(str(CalEntry[1]))
        MDEntry.write(')')
    # Co Authors
    if CalEntry[4] and CalEntry[4] != '' and CalEntry[4] != 'N/A' :
        MDEntry.write('\n\n')
        MDEntry.write('*Joint work with:* ')
        MDEntry.write(CalEntry[4])
    # Abstract
    if CalEntry[5] and CalEntry[5] != 'TBD' :
        MDEntry.write('\n\n')
        MDEntry.write(CalEntry[5])
    # Link
    if CalEntry[7] and CalEntry[7] != 'TBD' :
        MDEntry.write('\n\n')
        MDEntry.write('[More information](')
        MDEntry.write(CalEntry[8])
        MDEntry.write(')')
    MDEntry.write('\n\n')
    
    # Closing and saving
    MDEntry.close()
