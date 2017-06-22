# This program takes in  information form the SQLite database and drafts form emails
# It drafts both an announcement that it is capable of sending out and also an automated reminder to people to 
# let us know about their abstracts, etc. 
# The automated reminder is actually sent.

import os
import sqlite3
import time
import datetime
from email.mime.text import MIMEText  
from email.header import Header
from email.header import decode_header
import smtplib
import codecs
import sys
from kitchen.text.converters import getwriter

# Suggested fix for printing unicode strings in terminal...
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

########## Functions ##########


# Function to compose announcement emails:
# Input: NextTwo - List of up to two lists: Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SlotType
#           Note: Confusingly, Slot and Number are the same thing, number is in the schema but slot is facing the public
#        Room - A unicode string with the room number
# Output: A properly encoded MIME object (this is the message)
def MakeAnnouncement(NextTwo,Room) :

    # Validating these are the same date
    if len(NextTwo) >= 2 :
        assert NextTwo[0][0] == NextTwo[1][0]
        assert len(NextTwo) == 2
    ####################
    # Intro paragraphs:

    # Date of next presentation:
    NextDate = time.strptime(NextTwo[0][0], "%Y-%m-%d")
    # Default for room 
    if Room is None or Room == u'' :
        Room = u'Lorch 201'

    ##########
    # If a sole seminar:
    if len(NextTwo)== 1 or NextTwo[0][0] != NextTwo[1][0] :

        # Things to announce:
        Title = NextTwo[0][2]
        Presenter = NextTwo[0][3]
        Abstract = NextTwo[0][4]
        CoAuthors = NextTwo[0][5]

        # Subject
        Subject = time.strftime("%A",NextDate) + u': ' + Presenter + ' - ' + Title
        
        # First body paragraph: 
        Paragraph1 = u'Please join us this ' + time.strftime('%A',NextDate) + u', ' + time.strftime('%B',NextDate) + u' ' + time.strftime('%d',NextDate) + u' to see ' + Presenter + u' present: ' + Title + '.'
        # Clause if joint authored
        if CoAuthors != '' and CoAuthors is not None:
            JointClause = u' This is joint work with ' + CoAuthors + '.'
        else :
            JointClause = ''
        Paragraph1 = Paragraph1 + JointClause

        # Abstract (if exists)
        if Abstract != '' and Abstract is not None:
            Abstract = 'Abstract: ' + Abstract + '\r\n'
        else :
            Abstract = ''
    ##########
    # If joint: 
    else:

        # Things to announce for each:
        Title1 = NextTwo[0][2]
        Presenter1 = NextTwo[0][3]
        Abstract1 = NextTwo[0][4]
        CoAuthors1 = NextTwo[0][5]
        
        Title2 = NextTwo[1][2]
        Presenter2 = NextTwo[1][3]
        Abstract2 = NextTwo[1][4]
        CoAuthors2 = NextTwo[1][5]

        print type(Presenter1)
        print type(Presenter2)
        # Subject
        Subject = u'Two seminars on ' + time.strftime('%A',NextDate) + u': ' + Presenter1 + u' and ' + Presenter2

        # First body paragraph: 
        Paragraph1 = 'This ' + time.strftime('%A',NextDate) + ', ' + time.strftime('%B',NextDate) + ' ' + time.strftime('%d',NextDate) + ' we will have two presentations in summer seminar. First, ' + Presenter1 + ' will present: ' + Title1 + '. Then, once the commotion dies down, ' + Presenter2 + ' will present: ' + Title2 + '.'

        # Clause if joint authored
        if CoAuthors1 != '' and CoAuthors2 == '' :
            JointClause = 'Note that the first presentation is joint work with ' + CoAuthors1 + '.'
        elif CoAuthors1 != '' and CoAuthors2 == '' :
            JointClause = 'Note that the second presentation is joint work with ' + CoAuthors2 + '.'
        elif CoAuthors1 != '' and CoAuthors2 != '' :
            JointClause = 'Note that the first presentation is joint work with ' + CoAuthors1 + ' and the second is joint with ' + CoAuthors2 + '.'
        else :
            JointClause = ''

        # Gathering first paragraph together:
        Paragraph1 = Paragraph1 + JointClause

        # Abstract if exists: 
        Abstract = ''
        if Abstract1 != '' and Abstract2 != '' :
            Abstract = 'Abstract for \'' + Title1 + '\': ' + Abstract1 + '\n\r' 
            Abstract = Abstract + '\n\r' + 'Abstract for \'' + Title2 + '\': ' + Abstract2 + '\n\r' 
        elif Abstract1 != '' :
            Abstract = 'Abstract for \'' + Title1 + '\': ' + Abstract1 + '\n\r'
        elif Abstract2 != '' :
            Abstract = 'Abstract for \'' + Title2 + '\': ' + Abstract2 + '\n\r'
        
        

    # Paragraph 2 is common to all seminars: 
    Paragraph2 = "We will meet at 11:30 am in " + Room + ". You can see the full schedule including more info about these presentations and other upcoming seminars at http://seminar.mikezabek.com." 

    ##########
    # Assembling message text: 
    MessageText = Paragraph1 + "\n\r" + Paragraph2 + "\n\r\n\r" + "Best,\n\rMike and Ari" + "\n\r\n\r" + Abstract 

    ##########
    # Making into MIME object
    assert type(Subject) == unicode
    assert type(MessageText) == unicode

    # Setting up message (MIME) object:
    Msg = MIMEText(MessageText, 'plain', 'utf-8')
    Msg['From'] = Header(u'UMSumSem <UMSumSem@gmail.com>','utf-8')
    Msg['Subject'] = Header(Subject,'utf-8')
    Msg['To'] = Header(u'umeconsumsem@googlegroups.com','utf-8')
    # PRODUCTION: Where to send this: 
    #Msg['To'] = Header(u'UM,'utf-8')

    return (Msg)

# This is the text of the message we will send to people (not including the subject)
# Input: List of: Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SlotType
#           Note: Confusingly, Slot and Number are the same thing, number is in the schema but slot is facing the public
# Output: String containing the check in message, which is hard coded
def MakeCheckInMessage(RawInfo) :
    ## Draft of message:
    MessageMainText = u'''Hi,

This is a just a quick message about updating your summer seminar information. We listed what we have at the end of this email. If there is anything you would like to update, you can go do that at the following address. If you leave a field blank on that site (without spaces) then we'll stick with the old information.  

https://goo.gl/forms/8e1vTI1B8MWjQwev1

Note that when you fill out the form, it's important you include the "IDNumber" that we list below. That will make it easy for us to update your data quickly. 

You should see the new information up on the website within a few hours, and definitely within a day or two. The info will also be in the email announcement that we send. Let us know if it takes more than two days for your info to update. 

If you know of people, like faculty, that you would like to attend, we encourage you to reach out to them. We will send one announcement the day before your seminar. It will only go to the summer seminar mailing list, though, so most faculty members won't receive it and some students might not either. Even if people get our messages we have found that personal messages are often more effective than our advertising. 

We are looking forward to your presentation!

Best,
Mike and Ari

P.S. If you would like to cancel your presentation, you can, but we would like for you to let us know sooner rather than later. Send us an email (at this address).

'''


    ## Current info, written as a dict
    Presentation = {'IDNumber' : RawInfo[8],'Date' : RawInfo[0],'PresentationNumber':RawInfo[1],'Presenter': RawInfo[3],'CoAuthors':RawInfo[5],'Title': RawInfo[2],'Abstract':RawInfo[4],'StandardOrHalf':RawInfo[7],'Email':RawInfo[6]}

    # Code to standardize things as strings for display
    for Field in Presentation :
      try :
        if Presentation[Field] is None:
           Presentation[Field] = u''
        elif isinstance(Presentation[Field],int) :
          Presentation[Field] = str(Presentation[Field])
        else :
          Presentation[Field] = Presentation[Field]
      except IndexError :
        Presentation[Field] = u''

    Info = "Here is the IDNumber and the info we are currently advertising:"
    for PieceOfInfo in  ['IDNumber','Date','PresentationNumber','Presenter','CoAuthors','Title','Abstract','StandardOrHalf','Email'] :
        if PieceOfInfo != 'Email' :
            Info+=u'\r\n'
            Info+=PieceOfInfo
            Info+=u': '
            Info+=Presentation[PieceOfInfo]

    MessageText = MessageMainText + Info;
    # Setting up message (MIME) object:
    Msg = MIMEText(MessageText, 'plain', 'utf-8')
    Msg['From'] = Header(u'UMSumSem <UMSumSem@gmail.com>','utf-8')
    Msg['Subject'] = Header(u'Checking up about your summer seminar presentation','utf-8')
    Msg['To'] = Header(Presentation['Email'],'utf-8')

    return (Msg)

# Updates based on announcement...
def UpdateListAnnounced(Date,SQLCon) :
    print Date
    SQLCur = SQLCon.cursor()
    SQLCur.execute('''UPDATE Schedule
                    SET AnnouncementDate = datetime('now')
                    WHERE Date = ?;''', 
                    (Date,))
    SQLCon.commit()
    SQLCur.close()
    print "Announcment added to Schedule for Date: ",Date


# Updates based on check ins...
def UpdateListCheckedIn(ScheduleID,SQLCon) :
    SQLCur = SQLCon.cursor()
    SQLCur.execute('''UPDATE Schedule
                    SET CheckInDate = datetime('now')
                    WHERE ScheduleID = ?;''', 
                    (ScheduleID,))
    SQLCon.commit()
    SQLCur.close()
    print "Check in added to Schedule for SchedID: ",ScheduleID


# Displays a message... 
def DisplayMessage(Msg):
        print "------------------------------------------------------------"
        print "Message: "
        print Msg.items()
        print 'Subject: ',decode_header(Msg['Subject'])
        print 'From: ',decode_header(Msg['From'])
        print 'To: ',decode_header(Msg['To'])
        print Msg.get_payload(decode=True)
        print "------------------------------------------------------------"

# This is a wrapper to call the bottom two programs and append the results together
def MakeAllMessages(CurrentDate,SQLCur) :
        # Announcements
        TimeBeforeToAnnounce = datetime.timedelta(days=1,hours=22,minutes=30)
        EarliestToAnnounce = CurrentDate + TimeBeforeToAnnounce
        AnnouncementDateRange = (CurrentDate,EarliestToAnnounce)
        Announcements = DefineAnnouncements(AnnouncementDateRange,SQLCur)

        # Check ins
        TimeBeforeToCheckIn = datetime.timedelta(days=7)
        EarliestToCheckIn = AnnouncementDateRange[0] + TimeBeforeToCheckIn
        CheckInDateRange = (AnnouncementDateRange[0],EarliestToCheckIn) 
        CheckIns = DefineCheckIns(CheckInDateRange,SQLCur)

        # Showing all, together
        print "----------------------------------------"
        print "Announcement messages and check in messages ready to go:"
        EmailsToSend = Announcements + CheckIns
        for Email in EmailsToSend :
            DisplayMessage(Email['msg'])

        return(EmailsToSend)

########################################
# DefineAnnouncments - Setting announcement messages:
# Input: AnnouncementDateRange - Two dates defining first and last dates of semianrs to announce
# Output: Announcements - list with zero or one dict of one or two seminars to announce:
#           Sub entries are:
#                   1. msg - The email message itself, encoded as utf-8 for all fields
#                   2. date - The date of the seminars
#                   3. type - 'Announcement'
#                   4. id - Set to -1 
def DefineAnnouncements(AnnouncementDateRange,SQLCur):
    ##########
    # Outputting up to two seminars that are today or tomorrow: 
    # Note that they need to be assigned to an email address and the 
    # presented cannot be "Open"
    print "----------------------------------------"
    print "Writing appropriate announcements (if any) for: ",AnnouncementDateRange
    print "----------------------------------------"

    # Fetching entries in the window, that are asigned to someone, where there has not already been an announcment
    SQLOut = SQLCur.execute('''SELECT Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SlotType,ScheduleID
                    FROM Schedule
                    WHERE datetime(Date,'+11 hours','+30 minutes') >= ?
                    AND datetime(Date,'+11 hours','+30 minutes') <= ?
                    AND AnnouncementDate IS NULL
                    AND Presenter != 'Open'
                    AND Email != ''
                    AND Email != 'umsumsem@gmail.com'
                    ORDER BY date(Date) ASC
                    Limit 2;''', 
                    AnnouncementDateRange)
    ToAnnounce =  SQLOut.fetchall()
    # Restricts to the first date taken out 
    if len(ToAnnounce) == 2 :
        if ToAnnounce[0][0] != ToAnnounce[1][0] :
            del ToAnnounce[1]
    print "Announcing : "
    for Entry in ToAnnounce :
        print Entry[6],' on ',Entry[0]

    # Making up email message, if needed
    if len(ToAnnounce) > 0 :
        # Getting room, if in reservation section
        RoomList = SQLCur.execute('''SELECT Room 
                                    FROM RoomReservations WHERE Date=?;''',
                                    (ToAnnounce[0][0],)).fetchall()
        if RoomList :
            print RoomList[0]
            Room = RoomList[0][0]
        else :
            Room = None

        # Calling function to compose email subject and body as tupple:
        Msg = MakeAnnouncement(ToAnnounce,Room)
        
        # Printing it
        print "Announcement message: "
        Announcement = [{'date':ToAnnounce[0][0],'id':-1,'msg':Msg,'type':'Announcement'}]
        print Announcement[0]
        DisplayMessage(Announcement[0]['msg'])
    else :
        # If no seminars, return an empty list
        Announcement = []

    return(Announcement)

########################################
# DefineCheckIns setting check in messages:
# Input: AnnouncementDateRange - Two dates defining first and last dates of semianrs to announce
# Output: Announcements - dict of one or two seminars to announce:
#           Sub entries are:
#                   1. msg - The email message itself, encoded as utf-8 for all fields
#                   2. date - The date fo the seminars
#                   3. type - 'Announcement'
#                   4. id - Set to -1 
def DefineCheckIns(CheckInDateRange,SQLCur):
    ## Check in messages:
    CheckIns = []

    ##########
    # Listing of people to check in with, along with info to update... 
    print "----------------------------------------"
    print "Writing check in messages for the following dates: ",CheckInDateRange
    print "----------------------------------------"
    # Valid entries, in the date range, where we have no tchecked in
    SQLToCheck = SQLCur.execute('''SELECT Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SlotType,ScheduleID
                    FROM Schedule
                    WHERE datetime(Date,'+11 hours','+30 minutes') >= ?
                    AND datetime(Date,'+11 hours','+30 minutes') <= ?
                    AND AnnouncementDate IS NULL
                    AND Email != ''
                    AND CheckInDate IS NULL
                    ORDER BY date(Date) ASC
                    Limit 2;''', 
                    CheckInDateRange)
    ToCheckInWith =  SQLToCheck.fetchall()
    print "Checking in with: "
    for Entry in ToCheckInWith :
        print Entry[6],' on ',Entry[0]
    
    for Entry in ToCheckInWith :
        AskMsg = MakeCheckInMessage(Entry)
        CheckInEmail = {'id':Entry[8],'date':Entry[0],'msg':AskMsg,'type':'CheckIn'}
        print CheckInEmail
        CheckIns.append(CheckInEmail)
    return(CheckIns)

########################################
# This sends the specified emails:
# I.e. Taking EmailsToSend and sending them, using smtp on the gmail account
#       Also reqiuires a password, etc. 
def SendEmails(EmailsToSend,SQLCon) :
    if len(EmailsToSend) > 0 :
        print "\n\r\n\r\n\r"
        print "--------------------------------------------------------------------------------"
        print "Sending email messages: "
        print "--------------------------------------------------------------------------------"

        # Setting up email account:
        # Note: If there are a lot of email messages (More than 20 or so), this may need to be done more than once
        try: 
            EmailSMTP = smtplib.SMTP('smtp.gmail.com:587')
            EmailSMTP.starttls()
            # Reading in password from file (this is not very secure)
            with open('../Forms/password','r') as f :
                print "Setting up email login for UMSumSem:"
                EmailSMTP.login('UMSumSem',f.readline())
            EmailSetup = True
        except : 
            print "Error with establishing email connection"
            EmailSetup = False

        if EmailSetup == True :
            # Sending the emails
            print "Sending messages"
            for Email in EmailsToSend :
                # Things that will be sent:
                Msg = Email['msg']
                Subject = decode_header(Msg['Subject'])[0][0]
                From = decode_header(Msg['From'])[0][0]
                To = decode_header(Msg['To'])[0][0]

                # Trying to sedn them
                print Subject,"|From:",From,"|To:",To
                try: 
                    EmailSMTP.sendmail(From,To,Msg.as_string())
                    print 'Message sent!'
                    EmailSent = True
                except: 
                    EmailSent = False
                    print 'WARNING: Error sending. Subject: ',decode_header(Msg['Subject']),"|To",decode_header(Msg['To'])[0][0]

                # Updating the dataset to say that they are sent:
                # TODO: What if one fails and not another?
                if EmailSent == True :
                    if Email['type'] == "Announcement" :
                        UpdateListAnnounced(Email['date'],SQLCon)
                    elif Email['type'] == "CheckIn" :
                        UpdateListCheckedIn(Email['id'],SQLCon)
                    print 'SQL updated!'
            EmailSMTP.quit()
            print "Email connection closed"

########## End Functions ##########




################################################################################
# This is basically the program to do all of this stuff:


######################################## 
# TESTING: This loops through future dates to see that thigns work properly
def test():
    print '********************************************************************************'
    print '* Performing checks'
    print '********************************************************************************'
    StartTime = datetime.datetime(2017,6,22)
    for FutureDays in range(7) :
        for FutureHours in range(26) :
            print "-------------------- Testing iteration --------------------"
            # Current date, for testing
            DeltaTime = datetime.timedelta(days=FutureDays,hours=FutureHours)
            CurrentDate = StartTime + DeltaTime

            #SQL Dataset:
            SQLCon = sqlite3.connect('../Database/Testing/SumSemData20170622.db')
        
            ## Getting announcements and check ins
            SQLCur = SQLCon.cursor()
            EmailsToSend = MakeAllMessages(CurrentDate,SQLCur)
            SQLCur.close()

            # Making sure they are sent to the test address:
            for Email in EmailsToSend:
                Email['msg'].replace_header('To',Header(u'zabek@protonmail.com','utf-8'))  


            ## Sending emails
            # Ensuring emails are sent to the testing address
            if len(EmailsToSend) > 0 :
                for Email in EmailsToSend:
                    assert decode_header(Email['msg']['To'])[0][0] == 'zabek@protonmail.com' 
                    assert len(decode_header(Email['msg']['To'])) == 1
            SendEmails(EmailsToSend,SQLCon)


# Call of the program, for actually sending emails... 
def production():
    print '********************************************************************************'
    print '* Sending out real emails'
    print '********************************************************************************'
    # Current date:
    CurrentDate = datetime.datetime.today()
    ######################################## 
    #SQL Dataset:
    SQLCon = sqlite3.connect('../Database/SumSemData.db')

    ## Getting announcements and check ins
    SQLCur = SQLCon.cursor()
    EmailsToSend = MakeAllMessages(CurrentDate,SQLCur)
    SQLCur.close()

    ## Sending emails
    SendEmails(EmailsToSend,SQLCon)



# Main function, will default to testing unless passed PRODUCTION as first argument
def main():
    print "********************************************************************************"
    print "* Begun email update program "
    if len(sys.argv) > 1 and sys.argv[1] == "PRODUCTION" :
        production()
    else :
        test()
    print "********************************************************************************"
    print "File completed"
    print "********************************************************************************"

if __name__ == '__main__':
    main()
