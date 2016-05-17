This is a series of python scripts to deal with form data, allocations of rooms and presenters, and announcements for summer seminar. It could very well be overkill for the purpose, but for me (Mike) it has made administering everything a lot easier, more effective (at times), and less time intensive. 

It is somewhat customized so unfortunately won't be of a huge amount of use (unmodified) to other people. It also is written by an economist... 

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

The makefile outlines how they run (using [make](http://swcarpentry.github.io/make-novice/)). 

