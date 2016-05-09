# Program that updates the dataset

import unicodecsv as csv
import csv
import sqlite3
import os

########################################
# SQL Dataset:
print 'Opening database...'
sqlconn = sqlite3.connect('SumSemData.db')
c = sqlconn.cursor()

## Creating new table:
#print 'Creating new table...'
#c.execute('''DROP TABLE IF EXISTS Signup;''')

# Schema (important):
c.execute('''CREATE TABLE IF NOT EXISTS Signup (Timestamp text NOT NULL, Username text NOT NULL, Uniquename char(8), Title text, Authors text, JobTalk text, Abstract text, SlotType text, Availability text, Comments text, PRIMARY KEY(Username, Timestamp))''')

########################################
# Pulling in CSV of form responses:
print 'Opening CSV file...'
with open('../Forms/SignupForm.csv', 'rb') as file:
    entries = csv.reader(file, delimiter=',',quotechar='"')

    # Inserting rows past the first one
    entrynum = 0 
    for entry in entries:
        if entrynum == 0 : 
            print 'Beginning to read entries...'
            #print 'First row:'
            #print '|'.join(entry)
        else :
            # Inserting into dataset:
            c.execute('''INSERT OR REPLACE INTO Signup(Timestamp,Username,Uniquename,Title,Authors,JobTalk,Abstract,SlotType,Availability,Comments) VALUES (?,?,?,?,?,?,?,?,?,?)''', entry)
        entrynum += 1

########################################
# Committing and closing
sqlconn.commit()
sqlconn.close()
print 'Completed insert into SQLite database'

