## Notes from execution on AWS

1. Software was Amazon linux
  - Needed to add some packages
  - Python additions for unicode (unicodecsv, regex)
    - Used $ pip install *module* --user 
      - (why user?)
  - Jekyll
    - Needed ruby, gcc, ruby developer tools
  - Needed to configure cron jobs to have the appropriate profile when running them
    - E.g. source /user/ec2-user/.bash_profile before each cron task
2. Instance size -- t2.micro was throttled for the allocation call, and was slow
  - Tried running on c4.large, and was about 10x faster (the same setup, via Amazon Machine Image) 
  - Likely can use c4.large for allocation, then t2.nano for maintenance
3. Storing an Amazon Machine Image for next year should make things just work...

## Possible improvements

1. Using jekyll may be kind of odd:
 - It probably would be easier to generate the site with Pelikin
 - It also may make sense to use Django to host, separately from the allocation
 

