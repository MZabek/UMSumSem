#!/usr/bin/env python
# coding=utf-8

# Program to make SQLite database of room reservations from csv file
# Mike Zabek
# Original: June 9, 2017

import unicodecsv as csv
import regex as re
import sqlite3
import os
import sys
from kitchen.text.converters import getwriter

# Suggested fix for printing unicode strings in terminal...
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def main(): 
    ########################################
    # SQL Dataset:

    # Making folders for database
    if not os.path.exists('../Database/'):
        os.makedirs('../Database/')
    # Opening
    print 'Opening database...'
    ## Testing
    #sqlconn = sqlite3.connect('../Database/Testing/17AllotmentSumSemData.db')
    ## Production
    sqlconn = sqlite3.connect('../Database/SumSemData.db')
    sqlconn.text_factory = unicode
    c = sqlconn.cursor()

    # Creating brand new table (and deleting the old one) for reservations 
    c.execute('''DROP TABLE IF EXISTS RoomReservations;''')
    c.execute('''CREATE TABLE IF NOT EXISTS RoomReservations 
                (Timestamp datetime DEFAULT CURRENT_TIMESTAMP, 
                Date text NOT NULL PRIMARY KEY,
                Room text,
                StartTime text DEFAULT "11:00 am",
                EndTime text DEFAULT "2:00 pm",
                Notes text);
                ''')


    ########################################
    # Pulling in CSV of reservations:
    # Note that this is dependent on the setup of the file
    print 'Opening CSV reservation file...'
    with open('../Forms/2017Reservations.csv', 'rU') as file:
        # Reading the data in, with uft-8 encoding (which is what google forms spits out)
        entries = csv.reader(file, delimiter=',',quotechar='"', encoding='utf-8')

        entrynum = 0 
        for entry in entries:
            # First row is headers, which should behave as expected...
            if entrynum == 0 : 
                print "--------------------------------------------------------------------------------"
                print 'Beginning to read entries...'
                print 'First row:'
                
                # Identifying questions (row headers):
                questions = entry
                print questions
            else :
                # Other rows are data
                print 'Other row:'
                #print '|'.join(entry)

                # Making dictionary of questions and answers (to parse things)
                this_answer =  dict(zip(questions, entry))
                print this_answer

                # These should all be unicode
                assert type(this_answer[questions[0]]) == unicode

                # Ensuring I have retained unicode
                for answer in this_answer :
                    assert type(this_answer[answer]) == unicode
                    assert type(answer) == unicode

                # Inserting into SQL database
                c.execute('''INSERT OR REPLACE INTO 
                            RoomReservations(Timestamp,Date,Room,StartTime,
                                                EndTime,Notes) 
                        VALUES (?,?,?,?,?,?)''',
                        (this_answer['Timestamp'],this_answer['Date'],
                        this_answer['Room'],this_answer['StartTime'],
                        this_answer['EndTime'],this_answer['Notes']))
            entrynum += 1

    ########################################
    # Committing and closing
    sqlconn.commit()
    sqlconn.close()
    print 'Completed insert into SQLite database'


if __name__ == '__main__':
    main()
