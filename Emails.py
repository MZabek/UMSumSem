# This program takes in  information form the SQLite database and drafts form emails
# It drafts both an announcement that it is capable of sending out and also an automated reminder to people to 
# let us know about their abstracts, etc. 
# The automated reminder is actually sent.

import os
import sqlite3
import time
from email.mime.text import MIMEText 
import smtplib
import codecs

########## Functions ##########


# Function to compose announcement emails:
# Input: NextTwo - SQL fetch all composed of: Date,Number,Title,Presenter,Abstract,CoAuthors,Room
#           Note: Confusingly, Slot and Number are the same thing, number is in the schema but slot is facing the public
# Output: Tupple with: 1. Subject 2. Body of message
def MakeAnnouncement(NextTwo) :
    ####################
    # Intro paragraphs:

    # Date of next presentation:
    NextDate = time.strptime(NextTwo[0][0], "%Y-%m-%d")
    # Room is assumed the same: 
    Room = NextTwo[0][6].encode('utf-8')

    ##########
    # If a sole seminar:
    if len(NextTwo)== 1 or NextTwo[0][0] != NextTwo[1][0] :

        # Things to announce:
        Title = NextTwo[0][2]
        Presenter = NextTwo[0][3]
        Abstract = NextTwo[0][4]
        CoAuthors = NextTwo[0][5]
        Room = NextTwo[0][6]
        if Room != "Lorch 301" :
            Room.append(' (Note the room change!)')

        # Subject
        Subject = "Summer seminar this " + time.strftime("%A",NextDate) + ": " + Presenter + " - " + Title
        
        # First body paragraph: 
        Paragraph1 = "Please join us this " + time.strftime("%A",NextDate) + ", " + time.strftime("%B",NextDate) + " " + time.strftime("%d",NextDate) + " to see " + Presenter + " present: " + Title 
        # Clause if joint authored
        if CoAuthors != "" :
            JointClause = "This is joint work with " + CoAuthors + "."
        else :
            JointClause = ""
        Paragraph1 = Paragraph1 + JointClause

        # Abstract (if exists)
        if Abstract != "" :
            Abstract = "Abstract: " + Abstract + "\n\r"
    ##########
    # If joint: 
    else:

        # Things to announce for each:
        Title1 = NextTwo[0][2].encode('utf-8')
        Presenter1 = NextTwo[0][3].encode('utf-8')
        Abstract1 = NextTwo[0][4].encode('utf-8')
        CoAuthors1 = NextTwo[0][5].encode('utf-8')
        
        Title2 = NextTwo[1][2].encode('utf-8')
        Presenter2 = NextTwo[1][3].encode('utf-8')
        Abstract2 = NextTwo[1][4].encode('utf-8')
        CoAuthors2 = NextTwo[1][5].encode('utf-8')

        # Subject
        Subject = "Two summer seminars on " + time.strftime("%A",NextDate) + ": " + Presenter1 + " and " + Presenter2

        # First body paragraph: 
        Paragraph1 = "This " + time.strftime("%A",NextDate) + ", " + time.strftime("%B",NextDate) + " " + time.strftime("%d",NextDate) + " we will have two presentations in summer seminar. First, " + Presenter1 + " will present: " + Title1 + ". Then, once the commotion dies down, " + Presenter2 + " will present: " + Title2 + "."

        # Clause if joint authored
        if CoAuthors1 != "" and CoAuthors2 == "" :
            JointClause = "Note that the first presentation is joint work with " + CoAuthors1 + "."
        elif CoAuthors1 != "" and CoAuthors2 == "" :
            JointClause = "Note that the second presentation is joint work with " + CoAuthors2 + "."
        elif CoAuthors1 != "" and CoAuthors2 != "" :
            JointClause = "Note that the first presentation is joint work with " + CoAuthors1 + " and the second is joint with " + CoAuthors2 + "."
        else :
            JointClause = ""

        # Gathering first paragraph together:
        Paragraph1 = Paragraph1 + JointClause

        # Abstract if exists: 
        Abstract = ""
        if Abstract1 != "" :
            Abstract = "Abstract for \"" + Title1 + "\": " + Abstract1 + "\n\r"
        if Abstract2 != "" :
            Abstract = "Abstract for \"" + Title2 + "\": " + Abstract2 + "\n\r"
        
        

    # Paragraph 2 is common to all seminars: 
    Paragraph2 = "We will meet at 11:30 am in " + Room + ". You can see the full schedule including more info about these presentations and other upcoming seminars at http://mzabek.github.io/UMSumSem/." 

    ##########
    # Assembling message text: 
    MessageText = Paragraph1 + "\n\r" + Paragraph2 + "\n\r" + "Best,\rMike and Ari\n\r" + Abstract 


    return (Subject,MessageText)

# This is the text of the message we will send to people (not including the subject)
# Input: None
# Output: String containing the check in message, which is hard coded
def MakeCheckInMessage() :
    # Draft of message:
    MessageMainText = """Hi,

This is a just a quick message to ask if you would like to update any information for your summer seminar presentation. Please take a look at the information below. If there is anything you would like to update, you can go do that at the following address. You can also add new information, like a link to the full paper. If you leave a field blank on that site (without spaces) then we'll stick with the old information. Note that you will have to be logged into google (possibly in a separate browser window) via your @umich.edu account for this to work. 

http://goo.gl/forms/VVKiGwkBlbz3NObV2" 

You should see the new information up on the website within a day or two. It will also be in the email announcement that we send. 

If you know of people, like faculty, that you would like to attend, we encourage you to reach out to them. We will send one announcement the day before your seminar. It will only go to the summer seminar mailing list, though, so most faculty members won't receive it and some students might not either. Even if people get our messages we have found that personal messages are often more effective than our advertising. 

In any case, we're looking forward to your presentation!

Best,
Mike and Ari

P.S. If you would like to cancel your presentation, you can, but we would like for you to let us know sooner rather than later. Send us an email (at this address).
P.S.S. If you are having trouble with the form, you can use the old, slightly less reliable, version that doesn't require you be logged in via your umich email: http://goo.gl/forms/QLBVCSh4BQmkf3p62

"""
    return MessageMainText
########## End Functions ##########









########################################
# Setting up connections to SQL and email account:

#SQL Dataset:
SQLCon = sqlite3.connect('SumSemData.db')
SQLCur = SQLCon.cursor()

# Setting up email account:
EmailSMTP = smtplib.SMTP('smtp.gmail.com:587')
EmailSMTP.starttls()
#Reading in password from file (this is not very secure)
with open('password','r') as f :
    print "Setting up email login for UMSumSem:"
    EmailSMTP.login('UMSumSem',f.readline())


########################################
# Seminar announcements: 

print "Sending appropriate announcements (if any): "

##########
# Determining who to send these to:
# Whole email list: 
SQLEmails = SQLCur.execute('''SELECT Email FROM EmailList;''')
List = SQLEmails.fetchall()
Recipients = []
for Entry in List :
    Recipients.append(Entry[0].encode('utf-8'))


##########
# Which seminars to announce: 
# Outputting up to two seminars that are today or tomorrow: 
# Note that they need to be assigned to an email address and the 
# presented cannot be "Open"
SQLOut = SQLCur.execute('''SELECT Date,Number,Title,Presenter,Abstract,CoAuthors,Room 
                FROM Schedule
                WHERE date(Date) >= date('now','localtime')
                AND date(Date) <= date('now','localtime','+1 day')
                AND EmailAnnouncement IS NULL
                AND Presenter != 'Open'
                AND Email != ''
                AND Email IS NOT NULL
                ORDER BY date(Date) ASC
                Limit 2;''')
NextTwo =  SQLOut.fetchall()


# Sending email message if needed:
if len(NextTwo) > 0:
    # Calling function to compose email subject and body as tupple:
    EmailSubstance = MakeAnnouncement(NextTwo)

    # Setting up message (MIME) object:
    Msg = MIMEText(EmailSubstance[1].encode('utf-8'), 'plain', 'utf-8')
    Msg['From'] = 'UMSumSem <UMSumSem@gmail.com>'
    Msg['To'] = ', '.join(Recipients)
    Msg['Subject'] = EmailSubstance[0]



    print "------------------------------------------------------------"
    print "Sending the following announcement message: "
    print Msg.items()
    print Msg.get_payload(decode=True).decode(Msg.get_content_charset())
    print "----------------------------------------"
    ######################
    ### Sending message via UMSumSem email:
    try :
        # Updating SQL based on successful sending of the email
        SQLCur.execute('''UPDATE Schedule SET EmailAnnouncement = datetime('now') WHERE Date == '%s';''' % (NextTwo[0][0],))
        SQLCon.commit()
        SQLCur.execute('''SELECT Date,EmailAnnouncement FROM Schedule WHERE Date == '%s';''' % (NextTwo[0][0],))
        print(SQLCur.fetchall())
        # Sending the email
        print "Whom the message should be sent to:"
        print Msg['To']
        EmailSMTP.sendmail('UMSumSem@gmail.com',Recipients,Msg.as_string())
        print "Announcement sent and SQL updated!"
    except : 
        print "ERROR! Ether email not sent or SQL not updated!"
else : 
    print "No announcements needed (according to the SQL statement)"

##########################################
### Asking for updated information:
print "Asking for updated information from people (if any): "

# Info for seminars that are between (inclusive) today and two weeks from now
# and which I have not asked about yet. 
SQLToAsk = SQLCur.execute('''SELECT Date,Number,Title,Presenter,Abstract,CoAuthors,Email,SlotType,CheckIn,Link 
                FROM Schedule
                WHERE date(Date) >= date('now','localtime')
                AND date(Date) <= date('now','localtime','+7 day')
                AND Email != ''
                AND Email IS NOT NULL
                AND CheckIn IS NULL;''')
for ToAsk in SQLToAsk.fetchall():

    # Things to work with:
    Presentation = {'Date' : ToAsk[0]}
    # Loops through filling the dict, ignoring index errors... 
    for Field in ['Title','Presenter','Abstract','CoAuthors','Email','SlotType','Slot','Link'] :
      if Field=='Slot' :
        entry = 1
      elif Field=='Title' :
        entry = 2
      elif Field=='Presenter' :
        entry = 3
      elif Field=='Abstract' :
        entry = 4
      elif Field=='CoAuthors' :
        entry = 5
      elif Field=='Email' :
        entry = 6
      elif Field=='SlotType' :
        entry = 7
      elif Field=='Link' :
        entry = 8
      else  :
        entry = None

      # Code to put in either text, number, or empty string if some type of empty:
      try :
        if ToAsk[entry] is None:
          Presentation[Field] = ''
        elif isinstance(ToAsk[entry],int) :
          Presentation[Field] = str(ToAsk[entry])
        else :
          Presentation[Field] = ToAsk[entry]
      except IndexError :
        Presentation[Field] = ''


    Info = "Here is the info we are currently advertising on the website:"
    for PieceOfInfo in Presentation :
        if PieceOfInfo != 'Email' :
            Info+='\r\n'
            Info+=PieceOfInfo
            Info+=': '
            Info+=Presentation[PieceOfInfo]

    MessageText = MakeCheckInMessage() + Info


    # Assembling the email:
    Msg = MIMEText(MessageText, 'plain', 'utf-8')
    Msg['Subject'] = 'Checking up about your presentation on ' + time.strftime("%m/%d",time.strptime(Presentation['Date'], "%Y-%m-%d"))
    Msg['From'] = 'UMSumSem <UMSumSem@gmail.com>'
    Msg['To'] = Presentation['Email']


    print "Check up message: "
    print Msg.items()
    print Msg.get_payload(decode=True).decode('utf-8')

    print "Exporting to file"
    FileOut = 'EmailDrafts/Ask' + time.strftime('%y%m%d') + '.txt'
    # Note: writing normal python decoded from utf-8 even though this theoretically can support unicode... can't get it to work
    with codecs.open(FileOut,mode='a+b',encoding='utf-8') as MsgFile:
        MsgFile.write('\r################################################################################')
        MsgFile.write('\rCheck up message: ')
        MsgFile.write('\r')
        MsgFile.write(str(Msg.items()))
        MsgFile.write('\r')
        MsgFile.write(Msg.get_payload(decode=True).decode('utf-8'))
                
    print "Sending:"
    try: 
        EmailSMTP.sendmail('UmSumSem@gmail.com',Presentation['Email'],Msg.as_string())
        SQLCur.execute('''UPDATE Schedule SET CheckIn = datetime('now','localtime') WHERE Date == '%s' AND Number == %r;''' % (ToAsk[0],ToAsk[1]))
    except : 
        print "Error with sending message or updating dataset!"

### Closing connections:
SQLCon.commit()
SQLCur.close()
EmailSMTP.close()

