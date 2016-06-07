# Program to create markdown schedule from SQLite schedule table
# Mike Zabek
# Original: May 17, 2016
# Takes the SumSemData.db Scheudle table and creates: 
#   ../Website/schedule.md and ../Website/_texts/____.md
#   These are things that will be on the website

import sqlite3
import sys
import re
import os

#SQL Database connection:
sqlconn = sqlite3.connect('SumSemData.db')
c = sqlconn.cursor()

################################################################################
# Full schedule:

# Opening
MDSchedule = open('../Website/schedule.md','w')
MDSchedule.write('---\n')
MDSchedule.write('layout: page\n')
MDSchedule.write('title: Full schedule\n')
MDSchedule.write('---\n')

# Getting entries from database
print "Making full schedule with the following dates:"
CalEntries = c.execute('''SELECT Date,Number,Presenter,Title,CoAuthors,Abstract,Room,SlotType,Link FROM Schedule ORDER BY Date ASC, Number ASC;''')
for CalEntry in CalEntries.fetchall() :

    #Stripping out year from date:
    Date = re.sub("2016-","",CalEntry[0])
    # Re-inserting months: 
    Date = re.sub("05-","May ",Date)
    Date = re.sub("06-","June ",Date)
    Date = re.sub("07-","July ",Date)
    Date = re.sub("08-","August ",Date)
    Date = re.sub("09-","September ",Date)
    print Date

    # Writing text to file:
    # Date
    MDSchedule.write('## ')
    MDSchedule.write(Date)
    # Slot, if needed
    if CalEntry[7] and CalEntry[7] == 'Half (40 minutes)' :
        MDSchedule.write(' (Slot ')
        MDSchedule.write(str(CalEntry[1]))
        MDSchedule.write(')')
    # Presenter
    MDSchedule.write(' - ')
    MDSchedule.write(CalEntry[2].encode('utf8'))
    # Title
    if CalEntry[3] and CalEntry[3] != 'TBD' :
        MDSchedule.write('\n\n### ')
        MDSchedule.write(CalEntry[3].encode('utf8'))
    # Co Authors
    if CalEntry[4] and CalEntry[4] != '' and CalEntry[4] != 'N/A' and CalEntry[4] != None :
        MDSchedule.write('\n\n')
        MDSchedule.write('*Joint work with:* ')
        MDSchedule.write(CalEntry[4].encode('utf8'))
    # Location
    if CalEntry[6] : 
        MDSchedule.write('\n\n')
        MDSchedule.write('*Location:* ')
        MDSchedule.write(CalEntry[6].encode('utf8'))
        if CalEntry[6] != "Lorch 301" :
            MDSchedule.write('\n\n**Note the change in location!**')
    # Abstract
    if CalEntry[5] and CalEntry[5] != 'TBD' :
        MDSchedule.write('\n\n')
        MDSchedule.write(CalEntry[5].encode('utf8'))
    # Link
    if CalEntry[8] and CalEntry[8] != 'TBD' :
        MDSchedule.write('\n\n')
        MDSchedule.write('[More information]('+CalEntry[8].encode('utf8')+')')
    MDSchedule.write('\n\n')

# Closing and saving:
MDSchedule.close()

################################################################################
# Specific entries for upcoming events

# Getting entries
CalEntries = c.execute('''SELECT Date,Number,Presenter,Title,CoAuthors,Abstract,Room,SlotType,Link FROM Schedule WHERE date(Date) >= date('now','localtime') AND date(Date) <= date('now','localtime','+14 days') ORDER BY date(Date,'localtime') ASC, Number ASC;''')
EntryNum = 0
TargetDir = '../Website/_texts/'

# Removing all files in the directory:
print "Removing the following files:"
filelist = [ f for f in os.listdir(TargetDir) if f.endswith(".md") ]
for f in filelist:
    FullFile = TargetDir + f
    print FullFile
    os.remove(FullFile)

print "Creating the following files: "
for CalEntry in CalEntries.fetchall() :
    EntryNum = EntryNum + 1

    # Filename to save as: 
    SaveAs = TargetDir
    SaveAs +=str(EntryNum).zfill(4)
    SaveAs +='.md'
    print SaveAs 


    #Stripping out year from date:
    Date = re.sub("2016-","",CalEntry[0])
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
    Title = Title +  " (" + Date + ")"

    # Opening and writing header:
    MDEntry = open(SaveAs,'w')
    MDEntry.write('---\n')
    MDEntry.write('layout: post\n')
    MDEntry.write('title: ')
    MDEntry.write(Title.encode('utf8'))
    MDEntry.write('\n')

    MDEntry.write('---\n')

    # Writing text to file:
    # Date
    MDEntry.write('## ')
    MDEntry.write(Date)
    # Slot, if needed
    if CalEntry[7] and CalEntry[7] == 'Half (40 minutes)' :
        MDEntry.write(' (Slot ')
        MDEntry.write(str(CalEntry[1]))
        MDEntry.write(')')
    # Presenter
    MDEntry.write(' - ')
    if CalEntry[2] :
      MDEntry.write(CalEntry[2].encode('utf8'))
    # Co Authors
    if CalEntry[4] and CalEntry[4] != '' and CalEntry[4] != 'N/A' :
        MDEntry.write('\n\n')
        MDEntry.write('*Joint work with:* ')
        MDEntry.write(CalEntry[4].encode('utf8'))
    # Location
    if CalEntry[6] : 
        MDEntry.write('\n\n')
        MDEntry.write('*Location:* ')
        MDEntry.write(CalEntry[6].encode('utf8'))
        if CalEntry[6] != "Lorch 301" :
            MDEntry.write('\n\n**Note the change in location!**')
    # Abstract
    if CalEntry[5] and CalEntry[5] != 'TBD' :
        MDEntry.write('\n\n')
        MDEntry.write(CalEntry[5].encode('utf8'))
    # Link
    if CalEntry[8] and CalEntry[8] != 'TBD' :
        MDEntry.write('\n\n')
        MDEntry.write('[More information](')
        MDEntry.write(CalEntry[8].encode('utf8'))
        MDEntry.write(')')
    MDEntry.write('\n\n')
    
    # Closing and saving
    MDEntry.close()
