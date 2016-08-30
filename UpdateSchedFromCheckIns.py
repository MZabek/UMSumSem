# Idea is to update the schedule and email list based on the google sheet... 
# Mike Zabek
# May 28, 2016

# This builds on the google api python quickstart quite heavily
# Requires the google-api-python-client
# E.G. pip install --upgrade google-api-python-client
# It also requires stored credentials (client_secret.json) and access to specified sheets

from __future__ import print_function
import httplib2

import os
import sqlite3
import time
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from email.mime.text import MIMEText 
import smtplib

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Python Schedule Updater'

# Information update spreadsheets:
UpdateOrigSheetID = '1GxSrtlP_2vIA5KDf38rYiQFpubAUruK42-qbcvkXosQ'
UpdateOrigRange = 'Form Responses 2!A2:J'
UpdateV2SheetID = '1XjpdZIvFDq03eDydJe9S2l7OGGrDv6aelngUU9eTZiM'
UpdateV2Range = 'Form Responses 1!A2:H'
Cancellations = {'Sheet':'1_p6Uq7p5M0SKnGo52rl-xPAMBdXMeEhyKlx21wHOz9o','Range':'Form Responses 1!A2:J'}

# Email sign up spreadsheet:
EmailSheetID = '1a7nFoFnyeRTC1lgVPV_q879xs0TGefAaeliissCLJXU'
EmailRange = 'Form Responses 1!A2:B'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    ########################################
    # Setting up connections to SQL and Google Sheets:

    #SQL Dataset:
    SQLCon = sqlite3.connect('SumSemData.db')
    SQLCur = SQLCon.cursor()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    ########################################
    # Updating information based on original Google sheet:
    # LEGACY/DEPRECIATED:
    print('Updating info based on original google sheet')
    result = service.spreadsheets().values().get(
        spreadsheetId=UpdateOrigSheetID, range=UpdateOrigRange).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print('Updating info for: %s presentation %s' % (row[1],row[2]))
            # Saving data in a dict
            # re statements are sanitizing quotes in input... Should do more in the future probably?
            try : 
                NewData = {'Title':re.sub('\'','\'\'',row[3])}
                NewData['Abstract'] = re.sub('\'','\'\'',row[4])
                NewData['Presenter'] = re.sub('\'','\'\'',row[5])
                NewData['CoAuthors'] = re.sub('\'','\'\'',row[6])
                NewData['Link'] = re.sub('\'','\'\'',row[7])
                NewData['Cancel'] = re.sub('\'','\'\'',row[8])
            except IndexError:
                #print('Note: some (right) columns in the spreadsheet are completely empty')
                #print('''This shouldn't be a problem''')
                pass

            # ID variables:
            # Converting month and day:
            MonthAndDay = row[1].split('/')
            DateString = '''2016-%02d-%02d''' % (int(MonthAndDay[0]),int(MonthAndDay[1]))
            # Number of the seminar:
            Number = int(row[2])

            # Test to see if id-ing things right:
            Entries = SQLCur.execute('''SELECT Title,Abstract,LastUpdated FROM Schedule WHERE Date=='%s' AND Number==%d;''' % (DateString,Number))
            # If a successful match and not updated after spreadsheet entry, 
            # then updating the dataset variable by variable (where there and not an empty string) 
            FetchedEntries = Entries.fetchall()
            # Testing only one match and not more up to date than old version
            if len(FetchedEntries) == 1 and (FetchedEntries[0][2] is None or time.strptime(row[0],"%m/%d/%Y %H:%M:%S")>=time.strptime(FetchedEntries[0][2],"%Y-%m-%d %H:%M:%S")) :
                if 'Title' in NewData and NewData['Title'] != '':
                    SQLCur.execute('''UPDATE Schedule SET Title='%s',LastUpdated=datetime('now') WHERE Date=='%s' AND Number==%d;''' % (NewData['Title'],DateString,Number))
                if 'Abstract' in NewData and NewData['Abstract'] != '':
                    SQLCur.execute('''UPDATE Schedule SET Abstract='%s',LastUpdated=datetime('now') WHERE Date=='%s' AND Number==%d;''' % (NewData['Abstract'],DateString,Number))
                if 'Presenter' in NewData and NewData['Presenter'] != '':
                    SQLCur.execute('''UPDATE Schedule SET Presenter='%s',LastUpdated=datetime('now') WHERE Date=='%s' AND Number==%d;''' % (NewData['Presenter'],DateString,Number))
                if 'CoAuthors' in NewData and NewData['CoAuthors'] != '':
                    SQLCur.execute('''UPDATE Schedule SET CoAuthors='%s',LastUpdated=datetime('now') WHERE Date=='%s' AND Number==%d;''' % (NewData['CoAuthors'],DateString,Number))
                if 'Link' in NewData and NewData['Link'] != '':
                    SQLCur.execute('''UPDATE Schedule SET Link='%s',LastUpdated=datetime('now') WHERE Date=='%s' AND Number==%d;''' % (NewData['Link'],DateString,Number))
                print('It looks like some stuff was updated')
                SQLCon.commit()
            elif len(FetchedEntries) == 0 :
                print("WARNING: This identifying information not found in database: %s Slot %s" % (row[1],row[2]))
                print("This may be due to a valid cancellation")
            elif len(FetchedEntries) > 1 :
                print("ERROR: More than one entry found in database")
                print("ERROR: Check this identifying information: %s Slot %s" % (row[1],row[2]))
            elif time.strptime(row[0],"%m/%d/%Y %H:%M:%S")<time.strptime(FetchedEntries[0][2],"%Y-%m-%d %H:%M:%S") :
                #print("Database updated since response entered, not updating")
                #print('''Last update of entry: %s | Information Update: %s'''% (FetchedEntries[0][2],row[0]))
                pass
            # Sending email to account if cancellation
            # fancy if is to account for cases where no value in this column
            if len(row) >= 9 and row[8] is not None and row[8] == 'Please cancel the presentation' :
                print('Presentation cancellation!')
                # Setting up email account:
                EmailSMTP = smtplib.SMTP('smtp.gmail.com:587')
                EmailSMTP.starttls()
                #Reading in password from file (this is not very secure)
                with open('password','r') as f :
                    print("Setting up email login for UMSumSem:")
                    EmailSMTP.login('UMSumSem',f.readline())

                # Setting up message (MIME) object:
                Msg = MIMEText('Look up the response of %s'.encode('utf-8'), 'plain', 'utf-8' % (row[0],))
                Msg['From'] = 'UMSumSem <UMSumSem@gmail.com>'
                Msg['To'] = 'UMSumSem <UMSumSem@gmail.com>'
                Msg['Subject'] = 'Seminar cancellation on %s' % (row[1],)
                # Sending
                try : 
                    EmailSMTP.sendmail(Msg['From'],Msg['To'],Msg.as_string())
                except :
                    print('ERROR: Email not sent')

    ########################################
    # Updating information based on Google sheet:
    print('Updating info based on google sheet version 2.0')
    result = service.spreadsheets().values().get(
        spreadsheetId=UpdateV2SheetID, range=UpdateV2Range).execute()
    values = result.get('values', [])
    valuelabels = ('Timestamp','Email','Date','Title','Abstract','Presenter','CoAuthors','Link')

    if not values:
        print('No data found.')
    else:
        for row in values:
            print('Updating info for: %s on %s' % (row[1],row[2]))

            # Saving data in a dict
            NewData = {'Timestamp': row[0]}
            FieldNum = 0
            for Field in row :
                # re statements are sanitizing quotes in input... Should do more in the future probably?
                NewData[valuelabels[FieldNum]]=re.sub('\'','\'\'',Field)
                FieldNum= FieldNum + 1

            # ID variables:
            # Converting month and day:
            MonthAndDay = NewData['Date'].split('/')
            DateString = '''2016-%02d-%02d''' % (int(MonthAndDay[0]),int(MonthAndDay[1]))

            # Id-ing one seminar and saving its info in Entries
            SQLCur.execute('''SELECT Date,Number,LastUpdated FROM Schedule WHERE Email=='%s';''' % (NewData['Email'],))
            Entries = SQLCur.fetchall()
            if len(Entries) == 1 :
                print('    Updating based on email only...')
            elif len(Entries) > 1 :
                print('    More than one match based on email, matching on date as well')
                SQLCur.execute('''SELECT Date,Number,LastUpdated FROM Schedule WHERE Email=='%s' AND Date=='%s';''' % (NewData['Email'],DateString))
                Entries = SQLCur.fetchall();
                assert len(Entries) <= 1
            elif len(Entries) == 0 :
                print('    ERROR: No seminar assigned to this email address')

            if len(Entries) == 1 :
                # Updating the entry with the information in NewData
                MatchedDate = Entries[0][0]
                MatchedNumber = Entries[0][1]
                MatchedLastUpdated = Entries[0][2]
                # Updating if info from google sheets is more recent
                if  MatchedLastUpdated is None or time.strptime(NewData['Timestamp'],"%m/%d/%Y %H:%M:%S")>=time.strptime(MatchedLastUpdated,"%Y-%m-%d %H:%M:%S") :
                    # Looking through all fields and updating if relevant new info:
                    for Field in NewData :
                        if NewData[Field] != '' and Field != 'Timestamp' and Field != 'Date' :
                            SQLCur.execute('''UPDATE Schedule SET %s='%s',LastUpdated=datetime('now','localtime') WHERE Date=='%s' AND Number==%d;''' % (Field,NewData[Field],MatchedDate,MatchedNumber))
                            print('        Updated: ',Field)
                    SQLCon.commit()
                    print('    New data committed')
                else :
                    print('    Database info is more up to date')
            elif len(Entries) == 0 :
                print('    WARNING: This identifying information not found in database: %s Slot %s' % (row[1],row[2]))
                print('    This may be due to a valid cancellation')
            else :
                print('    ERROR: Could not find unique match for this info')

    ########################################
    # Cancellations
    print('Updating info from cancellations listing')
    result = service.spreadsheets().values().get(
        spreadsheetId=Cancellations['Sheet'], range=Cancellations['Range']).execute()

    values = result.get('values', [])
    valuelabels = ('Timestamp','Username','Email','Date','Slot','Comments','Re-allocation','NewEmail','NewComments','NewPresenter')


    if not values:
        print('No data found.')
    else:
        for row in values:
            print('Canceling seminar: %s on %s' % (row[2],row[3]))

            # Saving data in a dict
            ToEnter = {'Timestamp': row[0]}
            FieldNum = 0
            for Field in row :
                # re statements are sanitizing quotes in input... Should do more in the future probably?
                if valuelabels[FieldNum] == 'Slot' :
                    ToEnter[valuelabels[FieldNum]]=int(Field)
                else :
                    ToEnter[valuelabels[FieldNum]]=re.sub('\'','\'\'',Field)
                FieldNum= FieldNum + 1

            # ID variables:
            # Converting month and day:
            MonthAndDay = ToEnter['Date'].split('/')
            DateString = '''2016-%02d-%02d''' % (int(MonthAndDay[0]),int(MonthAndDay[1]))
            Number = ToEnter['Slot']

            # Finding the Entry
            SQLCur.execute('''SELECT Email,Date,Number,Cancellation,LastEmail FROM Schedule WHERE Email=='%s' AND Date=='%s' AND Number==%d;''' % (ToEnter['Email'],DateString,ToEnter['Slot']))
            Entries = SQLCur.fetchall()



            # Updating if not already updated and checking for errors in SQL
            if len(Entries) == 1 and Entries[0][3] is not None and time.strptime(ToEnter['Timestamp'],"%m/%d/%Y %H:%M:%S") < time.strptime(Entries[0][3],"%Y-%m-%d %H:%M:%S"):
                print('Timestamp is too old')
            elif len(Entries) == 0 :
                print('Entry not found, probably already cancelled')
            elif len(Entries) == 1 and ToEnter['Re-allocation'] == 'Assign to a new email' :
                SQLCur.execute('''UPDATE Schedule SET Email='%s',Presenter='%s',Title='',Abstract='',Link=NULL,CoAuthors='',Cancellation=datetime('now'),LastEmail=Email,LastUpdated=datetime('now'),EmailAnnouncement=NULL,CheckIn=NULL,Misc=NULL,WebPost=NULL WHERE Email=='%s' AND Date=='%s' AND Number==%d;''' % (ToEnter['NewEmail'],ToEnter['NewPresenter'],ToEnter['Email'],DateString,Number))
                SQLCon.commit()
                print('Entry switched to new presenter, %s' % (ToEnter['NewEmail'],))
            elif len(Entries) == 1 and ToEnter['Re-allocation'] == 'Post as open' :
                SQLCur.execute('''UPDATE Schedule SET Email='',Presenter='Open',Title='',Abstract='',Link=NULL,CoAuthors='',Cancellation=datetime('now'),LastEmail=Email,LastUpdated=datetime('now'),EmailAnnouncement=NULL,CheckIn=NULL,Misc=NULL,WebPost=NULL WHERE Email=='%s' AND Date=='%s' AND Number==%d;''' % (ToEnter['Email'],DateString,Number)) 
                SQLCon.commit()
                print('Entry switched to open')
            elif len(Entries) == 1 and ToEnter['Re-allocation'] == 'Delete the entry' :
                SQLCur.execute('''DELETE FROM Schedule WHERE Email=='%s' AND Date=='%s' AND Number==%s;''' % (ToEnter['Email'],DateString,Number)) 
                SQLCon.commit()
                print('Entry deleted')
            elif len(Entries) > 1 :
                print('ERROR: Multiple entries found')
            else :
                print('ERROR: Something went wrong in the logic of the cancellation update!')
                



    ########################################
    # Email signup
    print('Updating email list')

    # Reading email signup values:
    EmailResult = service.spreadsheets().values().get(
        spreadsheetId=EmailSheetID, range=EmailRange).execute()
    values = EmailResult.get('values', [])
    # For each row attempting to insert, will fail if already in there
    for row in values:
        try :
            with SQLCon :
                SQLCur.execute('''INSERT INTO EmailList (Timestamp,Email) VALUES (strftime('%m/%d/%Y %H:%M:%S','now'),?);''', (row[1],))
                SQLCon.commit()
                print('Added entry')
                print(row)
        except sqlite3.IntegrityError :
            pass
            #print('Already there')

if __name__ == '__main__':
    main()

