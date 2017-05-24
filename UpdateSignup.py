#!/usr/bin/env python
# coding=utf-8

# Program to make SQLite database from signup forms
# Mike Zabek
# Original: May, 2015
# Updated for the 2017 season

import unicodecsv as csv
import regex as re
import sqlite3
import os

# Setting piping encoding to unicode
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

########################################
# SQL Dataset:

# Making folders for database
if not os.path.exists('../Database/'):
    os.makedirs('../Database/')
# Opening
print 'Opening database...'
sqlconn = sqlite3.connect('../Database/SumSemData.db')
sqlconn.text_factory = unicode
c = sqlconn.cursor()

## MODIFY: Creating brand new tables for signup and email:
c.execute('''DROP TABLE IF EXISTS Signup;''')
c.execute('''CREATE TABLE IF NOT EXISTS Signup 
            (SignupID INTEGER PRIMARY KEY, Timestamp text NOT NULL, Username text NOT NULL, 
            Title text, Presenter text, CoAuthors text, SlotType text, JobTalk text, 
            Abstract text, PreferredDates text, WorkableDates text, Comments text, 
            InsertedTimestamp datetime DEFAULT CURRENT_TIMESTAMP)''')

c.execute('''DROP TABLE IF EXISTS EmailList;''')
c.execute('''CREATE TABLE IF NOT EXISTS EmailList 
            (SignupTimestamp text,  InsertedTimestamp datetime DEFAULT CURRENT_TIMESTAMP, 
            Email text NOT NULL PRIMARY KEY)''')

########################################
# Pulling in CSV of form responses:
# Note that this is dependent on the setup of the file
print 'Opening CSV main signup file...'
with open('../Forms/2017 SignupForm.csv', 'rU') as file:
    # Reading the data in, with uft-8 encoding (which is what google forms spits out)
    entries = csv.reader(file, delimiter=',',quotechar='"', encoding='utf-8')


    # Inserting rows past the first one
    entrynum = 0 
    for entry in entries:
        if entrynum == 0 : 
            print "--------------------------------------------------------------------------------"
            print 'Beginning to read entries...'
            print 'First row:'

            # Identifying questions (row headers):
            questions = entry
            print questions
        else :
            #print 'Other row:'
            #print '|'.join(entry)

            # Making dictionary of questions and answers (to parse things)
            this_answer =  dict(zip(questions, entry))
            # These should all be unicode
            #print type(this_answer)
            assert type(this_answer[questions[0]]) == unicode


            ## MODIFY: Making up avaiability list (comma separated list of specific dates):
            # NOTE: This is horribly inefficieint, but it is done very few times
            # Will populate list of preferred_dates and workable_dates, then turn into a string
            preferred_datel = [] 
            workable_datel = [] 
            for question in questions:
                # MODIFY: Looking through question list, to find date questions and see if preferred or workable
                if re.search("^Dates that work \[", question):
                    tempdatevalue = re.sub(u"^Dates that work \[","", question)
                    datevalue = re.sub("]$","", tempdatevalue)
                    if this_answer[question] == "Preferred":
                        preferred_datel.append(datevalue)
                    if this_answer[question] == "Workable":
                        workable_datel.append(datevalue)

            # Making a comma separated string of dates that work
            preferred_dates = ';'.join(preferred_datel)
            workable_dates = ';'.join(workable_datel)

            print "--------------------------------------------------------------------------------"
            print "Entry with preferred and workable dates:"
            print this_answer['Your name']
            print preferred_dates
            print workable_dates

            # Ensuring I have retained unicode
            for answer in this_answer :
                assert type(answer) == unicode
            assert (type(preferred_dates) == unicode) | (preferred_dates == '')


            ## MODIFY:  Inserting into dataset:
            c.execute('''INSERT OR REPLACE INTO 
                        Signup(Timestamp,Username,Presenter,Title,Abstract,CoAuthors,SlotType,
                        JobTalk,PreferredDates,WorkableDates,Comments) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                    (this_answer['Timestamp'],this_answer['Username'],this_answer['Your name'],
                        this_answer['Title of your presentation'],
                        this_answer['Abstract (if available)'],
                        this_answer['Other authors of the paper (not the presenter)'],
                        this_answer['Would you like a standard or a half slot?'],
                        this_answer['Is this a practice job talk?'],
                        preferred_dates,workable_dates,
                        this_answer['Comments for the organizers']))
            c.execute('''INSERT OR REPLACE INTO EmailList(SignupTimestamp,Email) 
                        VALUES (?,?)''', 
                        (this_answer['Timestamp'],this_answer['Username']))
        entrynum += 1

print 'Opening CSV email signup file...'
with open('../Forms/2017 Email signup.csv', 'rU') as file:
    entries = csv.reader(file, delimiter=',',quotechar='"',encoding='utf_8')

    # Inserting rows past the first one
    entrynum = 0 
    for entry in entries:
        if entrynum == 0 : 
            print 'Beginning to read entries...'
            print 'First row:'
            print '|'.join(entry)
        else :
            print "--------------------------------------------------------------------------------"
            print entry
            for element in entry:
                assert type(element) == unicode
            # Inserting into dataset:
            c.execute('''INSERT OR REPLACE INTO EmailList(SignupTimestamp,InsertedTimestamp,Email) 
                        VALUES (?,CURRENT_TIMESTAMP,?)''', entry)
        entrynum += 1





########################################
# Committing and closing
sqlconn.commit()
sqlconn.close()
print 'Completed insert into SQLite database'

