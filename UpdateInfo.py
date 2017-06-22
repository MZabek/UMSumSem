# Idea is to update the schedule and email list based on the google sheet... 
# Mike Zabek
# May 28, 2016

# This builds on the google api python quickstart quite heavily
# Requires the google-api-python-client
# E.G. pip install --upgrade google-api-python-client
# It also requires stored credentials (client_secret.json) and access to specified sheets

# Note: This has not been as heavily tested as other things... 
# TODO: Add in schema entry for UpdatedDate and use it here, much like CancellationDate

from __future__ import print_function
import httplib2

import os
import sqlite3
import time
import re
import datetime
import sys
from kitchen.text.converters import getwriter


from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# Suggested fix for printing unicode strings in terminal...
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None




def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    CLIENT_SECRET_FILE = '../Forms/client_secret.json'
    APPLICATION_NAME = 'Python Schedule Updater'


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
    print('\n\r\n\r')
    print('********************************************************************************')
    print(datetime.datetime.now())


    ########################################
    # Setting up connections to SQL and Google Sheets:

    # Year for dates:
    Year = datetime.datetime.now().year
    #SQL Dataset:
    # Testing SQLCon = sqlite3.connect('../Database/Testing/17AllotmentSumSemData.db')
    # Production 
    SQLCon = sqlite3.connect('../Database/SumSemData.db')
    SQLCur = SQLCon.cursor()

    # Google sheets connection:
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    ########################################
    # Updating information based on original Google sheet:
    print('\n\r\n\r')
    print('--------------------------------------------------------------------------------')
    print('Updating seminar info from responses')

    ## Opening up google sheet, and getting update requests...
    Updates = {'Sheet':'1tT4nxXYY1PWijkalquBoOkIVeACUYvy-CnuX0ARnUnU','Range':'Form Responses 1!A1:H'}
    result = service.spreadsheets().values().get(
        spreadsheetId=Updates['Sheet'], range=Updates['Range']).execute()
    Updates['Values'] = result.get('values', [])
    Updates['Labels'] = Updates['Values'][0]
    del Updates['Values'][0]
    print('Data we have:')
    print(Updates['Labels'])


    ## Updating entries based on the info in the sheet:
    for row in Updates['Values']:
        print('---------Updating info for one row-----------')

        ## Data processing:
        # Saving data in a dict
        ToEnter = {'Timestamp': row[0]}
        FieldNum = 0
        for Field in row :
            # re statements are sanitizing quotes in input... Should do more in the future probably?
            if (Updates['Labels'][FieldNum] == u'Which slot?') | (Updates['Labels'][FieldNum] == u'What is the IDNumber?')  :
                ToEnter[Updates['Labels'][FieldNum]]=int(Field)
            else :
                ToEnter[Updates['Labels'][FieldNum]]=re.sub('\'','\'\'',Field)
            FieldNum= FieldNum + 1

        # Converting month and day:
        try :
            MonthAndDay = ToEnter['What day is your seminar scheduled for?'].split('/')
            DateUString = u'''%04d-%02d-%02d''' % (int(Year),int(MonthAndDay[0]),int(MonthAndDay[1]))
            ToEnter['DateUString'] = DateUString
        except KeyError:
            print('No date was entered (probably fine)')

        print(ToEnter)
        print(ToEnter['Timestamp'],'|',ToEnter['What is the IDNumber?'])

        ## Finding the entry to update:
        Entries = SQLCur.execute('''SELECT Title,Abstract,CancellationDate
                                    FROM Schedule 
                                    WHERE ScheduleID ==?;''', (ToEnter['What is the IDNumber?'],))
        FetchedEntries = Entries.fetchall()

        # Updating the dataset, if one match and entery was not cancelled after its appearance on the sheet:
        if len(FetchedEntries) == 1  and FetchedEntries[0][2] is None or time.strptime(ToEnter['Timestamp'],'%m/%d/%Y %H:%M:%S') > time.strptime(FetchedEntries[0][2],'%Y-%m-%d %H:%M:%S') :
            # Printing info about what was found
            print('This is the entry to be updated:')
            print(FetchedEntries[0][0])
            
            # Validating that everything is the correct type
            for Entry in FetchedEntries[0] :
                if Entry :
                    assert type(Entry) == unicode or type(Entry) == int
            for Field in ToEnter :
                if ToEnter[Field] :
                    assert type(ToEnter[Field]) == unicode or type(ToEnter[Field]) == int

            # Writing entries
            if 'Title' in ToEnter and ToEnter['Title'] != '':
                SQLCur.execute('''UPDATE Schedule 
                                    SET Title=? 
                                    WHERE ScheduleID ==?
                                ;''', (ToEnter['Title'],ToEnter['What is the IDNumber?']))
                print(u'Title|',ToEnter['Title'])
            if 'Abstract' in ToEnter and ToEnter['Abstract'] != '':
                SQLCur.execute('''UPDATE Schedule 
                                    SET Abstract=?
                                    WHERE ScheduleID ==?
                                ;''', (ToEnter['Abstract'],ToEnter['What is the IDNumber?']))
                print(u'Abstract|',ToEnter['Abstract'])
            if 'Presenter' in ToEnter and ToEnter['Presenter'] != '':
                SQLCur.execute('''UPDATE Schedule 
                                    SET Presenter=? 
                                    WHERE ScheduleID==?
                                ;''', (ToEnter['Presenter'],ToEnter['What is the IDNumber?']))
                print(u'Presenter|',ToEnter['Presenter'])
            if 'Co-authors' in ToEnter and ToEnter['Co-authors'] != '':
                SQLCur.execute('''UPDATE Schedule 
                                    SET CoAuthors=?
                                    WHERE ScheduleID==?
                                ;''', (ToEnter['Co-authors'],ToEnter['What is the IDNumber?']))
                print(u'Co-authors|',ToEnter['Co-authors'])
            SQLCon.commit()
            print('Finished updating with no errors')
        elif len(FetchedEntries) == 0 :
            print('WARNING: This identifying information not found in database: %s' % (ToEnter['What is the IDNumber?']))
            print('This may be due to a valid cancellation')
        elif len(FetchedEntries) > 1 :
            print('ERROR: More than one entry found in database')
            print('ERROR: Check this identifying information: %s ' % (ToEnter['What is the IDNumber?']))
        elif FetchedEntries[0][2] is not None and time.strptime(ToEnter['Timestamp'],'%m/%d/%Y %H:%M:%S') <= time.strptime(FetchedEntries[0][2],'%Y-%m-%d %H:%M:%S') :
            print('WARNING: this seminar was subsequently cancelled')


    ########################################
    # Cancellations

    print('\n\r\n\r')
    print('--------------------------------------------------------------------------------')
    print('Updating info from cancellations listing')


    ## Getting whole list of cancellation data from google... 
    Cancellations = {'Sheet':'1hvwg1g8OkgemmyNuSBEsYFa99VIE0Jq2x14sSpmDPWs','Range':'Form Responses 1!A1:J'}

    ## Getting cancellations listing:
    result = service.spreadsheets().values().get(
        spreadsheetId=Cancellations['Sheet'], range=Cancellations['Range']).execute()

    CancelationData = result.get('values', [])
    CancelationLabels = CancelationData[0]
    del CancelationData[0]
    print('Data we have:')
    print(CancelationLabels)

    ## Processing each row of the cancelation data:
    for row in CancelationData:
        print('--------------------')

        ## Data processing:
        # Saving data in a dict
        ToEnter = {'Timestamp': row[0]}
        FieldNum = 0
        for Field in row :
            # re statements are sanitizing quotes in input... Should do more in the future probably?
            if CancelationLabels[FieldNum] == 'Slot' :
                ToEnter[CancelationLabels[FieldNum]]=int(Field)
            else :
                ToEnter[CancelationLabels[FieldNum]]=re.sub('\'','\'\'',Field)
            FieldNum= FieldNum + 1

        # Converting month and day:
        MonthAndDay = ToEnter['Date'].split('/')
        DateUString = u'''%04d-%02d-%02d''' % (int(Year),int(MonthAndDay[0]),int(MonthAndDay[1]))
        ToEnter['DateUString'] = DateUString

        ## Finding the relevant entry
        # Finding the Entry
        print('Finding:',ToEnter['Email'],ToEnter['DateUString'],ToEnter['Slot'])
        SQLCur.execute('''SELECT Email,Date,Number,CancellationDate
                            FROM Schedule 
                            WHERE Email == ? AND Date==? AND Number==?
                        ;''', (ToEnter['Email'],ToEnter['DateUString'],ToEnter['Slot']))
        Entries = SQLCur.fetchall()
        print('This is what I found:',Entries)
        if len(Entries) == 0 :
            SQLCur.execute('''SELECT Email,Date,Number,CancellationDate
                                FROM Schedule 
                                WHERE Email == 'umsumsem@gmail.com' AND Date==? AND Number==?
                            ;''', (ToEnter['DateUString'],ToEnter['Slot']))
            Entries = SQLCur.fetchall()
            print('This is what I found with the umsumsem@gmail.com address:',Entries)
            # Setting the other email address to be the one to search for below
            if len(Entries) == 1 :
                ToEnter['Email'] = Entries[0][0]


        ## Updating if not already updated and checking for errors in SQL
        if len(Entries) == 1 and Entries[0][3] is not None and time.strptime(ToEnter['Timestamp'],'%m/%d/%Y %H:%M:%S') < time.strptime(Entries[0][3],'%Y-%m-%d %H:%M:%S'):
            print('Already updated: timestamp is older than CancellationDate in the database')
        elif len(Entries) == 0 :
            print('Entry not found, perhaps it was already cancelled')
        elif len(Entries) == 1 and ToEnter['Re-allocate the slot?'] == 'Assign to a new email' :
            SQLCur.execute('''UPDATE Schedule 
                                SET Email=?,Presenter=?,CancellationDate=datetime('now'),
                                    LastEmail=Email,
                                    Title=NULL,Abstract=NULL,CoAuthors=NULL,AnnouncementDate=NULL,CheckInDate=NULL 
                                WHERE Email==? AND Date==? AND Number==?
                            ;''', (ToEnter['New email'],ToEnter['New presenter'],ToEnter['Email'],ToEnter['DateUString'],ToEnter['Slot']))
            SQLCon.commit()
            print('Entry switched to new presenter, %s' % (ToEnter['New email'],))
        elif len(Entries) == 1 and ToEnter['Re-allocate the slot?'] == 'Post as open' :
            SQLCur.execute('''UPDATE Schedule SET Email='umsumsem@gmail.com',Presenter='Open',Title=NULL,Abstract=NULL,
                                                CoAuthors=NULL,CancellationDate=datetime('now'),
                                                LastEmail=Email,Link=NULL,
                                                Title=NULL,Abstract=NULL,CoAuthors=NULL,
                                                AnnouncementDate=NULL,CheckInDate=NULL 
                                            WHERE Email==? AND Date==? AND Number==?
                            ;''', (ToEnter['Email'],ToEnter['DateUString'],ToEnter['Slot'])) 
            SQLCon.commit()
            print('Entry switched to open')
        elif len(Entries) == 1 and ToEnter['Re-allocate the slot?'] == 'Delete the entry' :
            SQLCur.execute('''DELETE FROM Schedule 
                                    WHERE Email==? AND Date==? AND Number==?
                            ;''', (ToEnter['Email'],ToEnter['DateUString'],ToEnter['Slot'])) 
            SQLCon.commit()
            print('Entry deleted')
        elif len(Entries) > 1 :
            print('ERROR: Multiple entries found')
        else :
            print('ERROR: Something went wrong in the logic of the cancellation update!')
            




if __name__ == '__main__':
    main()

