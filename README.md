# Using PeopleSoft

PeopleSoft is a curse on humanity.  

I'm not even sure what "PeopleSoft" (PS) entails, but the curse for me is the web-based user interface to CRUD on the backend database. I actually feel sorry for anyone who uses it, and you can spot it a mile away. The tight, small fonts and little boxes littered all over the screen. There's no responsive behavior, it's ugly, slow and unintuitive. Boxes are too small for content they are to hold, and no one can fix this. Then there's the dreaded spinners and apparent, calls to the server as focus for each entry element is changed, and lack of a "save an exit" button (it's always click to 'Save' then another click to exit. And, the "Are you sure you want to exit" warning doesn't have a "Save and Exit" option).  

No one should be forced to use such an awful interface, but a lot of us have to, since it's the backend that runs many large organizations. In my case, a major American university. I must use PS to tell the university about my local department's scheduling plans for upcoming terms (what classes, where, times of day, intructor names, etc.). From here, the data goes to student registration pages (also some derivative of PS), payroll, etc. Yuk.

Internally, I am able to create a CSV file containing all information about my department's upcoming course offerings. Something like this:

ASTR-101,01,01,LEC,053 -0215,MTWR,03:10 PM,04:00 PM,Y,70,E,last1,first1,emplid1,,
ASTR-102,01,01,LEC,,MTWR,,,Y,120,E,last2,first2,emplid1,,
ASTR-102,02,02,LEC,053 -0206,MTWR,04:10 PM,05:00 PM,Y,70,E,Shlaer,Ben,emplid1,,
ASTR-324,01,01,LEC,053 -0215,MTWR,01:10 PM,02:00 PM,Y,48,E,Bensky,Tom,emplid1,,
GEOL-102,01,01,LEC,,MW,07:40 AM,09:00 AM,Y,120,E,Jasbinsek,John J.,emplid1,,
GEOL-102,02,9999,DIS,180 -0233,W,10:10 AM,11:00 AM,Y,30,N,Jasbinsek,John J.,emplid1,,
