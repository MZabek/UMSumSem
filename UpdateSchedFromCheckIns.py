# Idea is to update the schedule and email list based on the google sheet... 
# Mike Zabek
# May 28, 2016

# This builds on the google api python quickstart quite heavily
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

# Information update spreadsheet:
UpdateSheetID = '1GxSrtlP_2vIA5KDf38rYiQFpubAUruK42-qbcvkXosQ'
UpdateRange = 'Form Responses 2!A2:J'

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
    """Updates schedule based on table and says so in the table...

    Creates a Sheets API service object and prints the names and majors of
    """


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

    print('Updating info based on google sheet')
    result = service.spreadsheets().values().get(
        spreadsheetId=UpdateSheetID, range=UpdateRange).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print('Updating info for: %s presentation %s' % (row[1],row[2]))
            # Saving data in a dict
            try : 
                NewData = {'Title':row[3]}
                NewData['Abstract'] = row[4]
                NewData['Presenter'] = row[5]
                NewData['CoAuthors'] = row[6]
                NewData['Link'] = row[7]
                NewData['Cancel'] = row[8]
            except IndexError:
                print('Note: some (right) columns in the spreadsheet are completely empty')
                print('''This shouldn't be a problem''')

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
            if len(FetchedEntries) == 1 and time.strptime(row[0],"%m/%d/%Y %H:%M:%S")>=time.strptime(FetchedEntries[0][2],"%Y-%m-%d %H:%M:%S") :
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
            elif time.strptime(row[0],"%m/%d/%Y %H:%M:%S")<time.strptime(FetchedEntries[0][2],"%Y-%m-%d %H:%M:%S") :
                print("Database updated since response entered, not updating")
                print('''Last update of entry: %s | Information Update: %s'''% (FetchedEntries[0][2],row[0]))
            elif len(FetchedEntries) != 1 :
                print("ERROR: Corresponding unique entry not found in database")
                print("ERROR: Check this identifying information: %s Slot %s" % (row[1],row[2]))


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
        except sqlite3.IntegrityError :
            print('''Already in the email list - %s''' % (row[1],))

if __name__ == '__main__':
    main()

