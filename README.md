# Using PeopleSoft

PeopleSoft is a curse on humanity.  

I'm not even sure what "PeopleSoft" (PS) entails, but the curse for me is the web-based user interface to CRUDing on the backend database. I actually feel sorry for anyone who uses it, and you can spot on a screen it a mile away. The tight, small fonts and little boxes littered all over the screen. There's no responsive behavior, it's ugly, slow and unintuitive. There's no modern look to the elements (a la Bootstrap, etc.), boxes are too small for content they are to hold, and changes are impossible to implement (PS is used by large organizations, with multiple levels of committees for approving fixes).

Then there's the dreaded spinners and calls to the server with each change of focus for each entry element (can you say "s-l-o-w?"). There's also no "save an exit" button (it's always click to save, then another click to exit. And, the "Are you sure you want to exit" warning doesn't have a "Save and Exit" option).  

No one should be forced to use such an awful interface, but a lot of us have to, since it's the backend that runs many large organizations. In my case, a major American university. I must use PS to tell the university about my local department's scheduling plans for upcoming terms (what classes, where, times of day, intructor names, etc.). From here, the data goes to student registration pages (also some derivative of PS), payroll, tuition bills, etc.

Internally, I am able to create a CSV file containing all information about my department's upcoming course offerings. Something like this:

```
ASTR-101,01,01,LEC,053 -0215,MTWR,03:10 PM,04:00 PM,Y,70,E,last1,first1,emplid1,,
ASTR-102,01,01,LEC,,MTWR,,,Y,120,E,last2,first2,emplid2,,
ASTR-102,02,02,LEC,053 -0206,MTWR,04:10 PM,05:00 PM,Y,70,E,last3,first3,emplid3,,
ASTR-324,01,01,LEC,053 -0215,MTWR,01:10 PM,02:00 PM,Y,48,E,last4,first4,emplid4,,
GEOL-102,01,01,LEC,,MW,07:40 AM,09:00 AM,Y,120,E,last5,first5,emplid5,,
GEOL-102,02,9999,DIS,180 -0233,W,10:10 AM,11:00 AM,Y,30,N,last6,first6,emplid6,,
...
...
...
```
This goes on typically for about 200 lines.  Here you can see classes, week days, times, etc. Making this CSV is also a lot of work, but more so on the side of planning.  (The genetic algorithm I used to do this planning is another topic.)  Nonetheless, this is our schedule, and it must go into PS by a certain deadline four times a year, once for each term. Yes a large portion of a previous term's data is rolled over, but with all of the small changes typically needed, this rollover is only marginally useful.  There is still much work to be done.  Further, data views in PS are non-existent, so you are forced to come up with your own. In my case, it's graphical drawings of rooms with classes tiled in them.  So then, I'm off into my own views and staying synced with PS becomes a huge issue. If I click to drag a class to an hour later in the day, and do this multiple times in my planning phase, how does this make it back into PS?

When I first started as my department's scheduler, I would print my final plan on paper, get out a ruler for keeping track, and type each line into PS. Usually to the tune of 180 classes or so. I know this is crazy, but in large organizations, printing data on one computer to enter into another computer is pretty common.

At one point a while back, I said "enough."  A friend who does web-development once showed me a testing tool called "Selenium," so I decided to take a look. It even says on their website "Boring web-based administration tasks can (and should) also be automated..."  This project shows how I use Selenium to read in my CSV and type it into PS for me.

# Selenium

[Selenium](https://www.selenium.dev) is some core of all of the popular web-browsers (Chrome, Firefox, Safari) that can be controlled via software. That means all clicks, fill-in boxes, 'save' buttons and the like can be triggered using software. I use the Python 'bindings' for it, and somehow when I run my Python script, a Chrome browser opens up that says "Chrome is being controlled by automated test software." This means two things: 1) The host server (i.e. PS) doesn't know anything unsual is going on--it's just Chrome afterall and 2) I don't click to control this browser; the Python script does.


# Automating
