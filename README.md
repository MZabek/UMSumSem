# Intro

This is a series of python scripts to deal with form data, allocations of rooms and presenters, and announcements for the University of Michigan summer seminar in economics. It could very well be overkill for the purpose, but for me (Mike) it has made administering everything a lot easier, more effective, and less time intensive. 

It is somewhat customized so unfortunately won't be of a huge amount of use (unmodified) to other people. It also is written by an economist as an attempt to learn gheneral python programming as well as SQL through SQLite. 

## Main idea

Broadly three things need to be done:

1. Making the initial schedule: 
   1. Taking in info from people wanting to present (at the beginning)
   2. Allocating people to rooms
   3. Posting the schedule in a way that people like
2. Updating the schedule
   1. Checking in with people about updated info
   2. Dealing with cancellations 
   3. Updating the schedule about each of the above 
3. Actually posting announcements/keeping people informed

This integrates with a UMSumSem gmail account (and drive folder) to do a good amount of the work for all of those things. 


## Files:

There are different sets of python scripts to do various things:

The makefile outlines how many of these processes run (using [make](http://swcarpentry.github.io/make-novice/)), with the big omission of the updating phase which depends on updates to the google forms data that make has trouble checking for. 

##### The Allocation phase:

1. The UpdateSignup.py takes a downloaded csv file (not the website) and updates the dataset
2. Allotment.py does the allotment... and puts it in the database

##### Posting the schedule online

This is done via the MakeMDSchedule, whihc makes some markdown documents that are then readable by jekyll, which is what github pages uses. I have a jekyll setup that I took from someone else for the website. 

This is re-done periodically. When it is done, new files have to be put there and then the changes have to be committed to the gh-pages branch of the github respository. The Jekyll stuff that I do, I think, is just so that I can view it locally before it goes up. I have never done it any other way, though, and I know nothing about ruby on rails or much of Jekyll. 

#####The Updating phase 
This is done by UpdaterScript.sh, which I run in the morning on most days, via a scheduled job.

1. Emails.py sends out emails that seem relevant at the moment it is executed. These include:
   - Announcements to the email list
   - Check ins to people with upcoming seminars
2. UpdateSchedFromCheckIns.py checks the google form online with responses from check ins and updates the database. 
   - As of 5/29 it does noting with cancelations, however. Keep this in mind.

##### Dependencies

I have tried to run this on a very old Ubuntu MATE laptop. I had to install: 

1. pip and google-api-python-client
2. instal bundle for ruby if you want to see the website locally (Is it possible to skip this in make file?)
   1. gem install bundle 
   2. bundle install in website directory (which is kinda problematic)

If I were super cool this might be in Docker? Or it would just live on the cloud in AWS?

## Things that have to be done manually:

We still haven't:

1. Figured out how to do cancelations quite fully. When this happens someone should ask the wait lsit for new takers.
2. Updating the wait list and email lists... 
   - Given the form, it might be easy to automate this in the near future... Not sure it's a huger return though. I have an orhpaned branch starting this. 
3. Deal with special cases and discretion.
4. Like, actually be there, etc.  
