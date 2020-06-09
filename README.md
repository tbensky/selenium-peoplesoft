# Using PeopleSoft

I've had to use PeopleSoft for part of my job for about 6 years now, and I've concluded that: PeopleSoft is a curse on humanity.  

I'm not even sure what "PeopleSoft" (PS) is, but the curse for me is the web-based user interface to CRUDing on a backend database. I actually feel sorry for anyone who uses PS and a lot of people do. You can spot on a screen it a mile away. The tight, small fonts and little boxes littered all over the screen. There's no responsive behavior, it's ugly, slow and unintuitive. There's no modern look to the elements (a la Bootstrap, etc.), boxes are too small for content they are to hold, and changes are impossible to implement, because PS is typically used by large organizations, with multiple levels of committees for approving fixes. I for example, would like the box that is to contain 5 letters (one for each day of the week), to be wide enough for all 5 letters at a time. Some text-entry boxes require one to input data in a certain format, which could be eliminated with a trivial form-data post-processing step of having the computer pad numbers with zeros and place a space between them.

Then there's the dreaded spinners and calls to the server with each focus change for a every entry element (=slow). There's also no "save and exit" button (it's always click to save, then another click to exit. And, the "Are you sure you want to exit" warning doesn't have a "Save, then Exit" option).  

No one should be forced to use such an awful interface, but a lot of us have to, since it's the backend that runs many large organizations. In my case, a major American university. I must use PS to tell the university about my local department's scheduling plans for upcoming terms (what classes, where, times of day, intructor names, etc.).  Once in a backend database, the data then goes to student registration pages (also some derivative of PS), payroll, tuition bills, etc. But of course it's refreshed, so you have to wait 24 hours for such down-stream changes.

# My data flow plan

Internally, as I create my department's schedule, I end up with a CSV file containing all information about my department's upcoming course offerings. Something like this:

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
This goes on typically for about 200 lines.  Here you can see classes, week days, times, etc. Making this CSV is also a lot of work, but more so on the side of planning.  (The genetic algorithm I used to do this planning is another topic.)  Nonetheless, this is our schedule, and it must go into PS by a certain deadline four times a year, once for each term. Yes a large portion of a previous term's data is rolled over, but with all of the small changes typically needed, this rollover is only marginally useful.  There is still much work to be done.  Further, data views in PS are non-existent, so you are forced to come up with your own. In my case, it's graphical drawings of rooms with classes tiled in them, created using scheduling software of my own design.  So then, I'm off into my own views and staying synced with PS becomes a huge issue. If I click to drag a class to an hour later in the day (and maybe do this countless times to tweak the schedule) in my planning phase, how does this make it back into PS?

When I first started as my department's scheduler, I would print my final plan on paper, get out a ruler for keeping track, and type each line into PS. Usually to the tune of 180 classes or so. I know this is crazy, but in large organizations, printing data on one computer to enter into another computer is pretty common. 

At one point a while back, I said "enough."  A friend who does web-development once showed me a testing tool called "Selenium," so I decided to take a look. It even says on their website "Boring web-based administration tasks can (and should) also be automated..."  This project shows how I use Selenium to read in my CSV and type it into PS for me.

# Selenium

[Selenium](https://www.selenium.dev) is some core of all of the popular web-browsers (Chrome, Firefox, Safari) that can be controlled via software. That means all clicks, fill-in boxes, 'save' buttons and the like can be triggered using software. I use the Python 'bindings' for it, and somehow when I run my Python script, a Chrome browser opens up that says "Chrome is being controlled by automated test software." This means two things: 1) The host server (i.e. PS) doesn't know anything unsual is going on--it's just Chrome afterall and 2) I don't click to control this browser; the Python script does.


# Automating

If you're curious, [the documentation](https://www.selenium.dev/documentation) for Selenium is excellent. This first Python example shows you the general plan:

```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC

#This example requires Selenium WebDriver 3.13 or newer
with webdriver.Chrome('/Users/tom/Dropbox/Selenium/chromedriver') as driver:
    wait = WebDriverWait(driver, 10)
    driver.get("https://google.com/ncr")
    driver.find_element(By.NAME, "q").send_keys("cheese" + Keys.RETURN)
    #first_result = wait.until(presence_of_element_located(By.CSS_SELECTOR, "h3>div"))
    first_result = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR , "h3>div")))
    print(first_result.get_attribute("textContent"))
```

Casually browsing the code, you can see how the page ```https://google.com/ncr``` is requested.  Google's search box is famously referred in the underlying HTML by the same of ```q```. You tell Selenium to find this element in the HTML data on Google's main search page (```find_element```).  Once found, into this element you have Selenium type, via the ```send_keys``` function, the text ```cheese``` followed by return. In other words, you are having Selenium search for the word ```cheese```--and you'll see it all happen in the automated Chrome view that the script will pop up on your screen.

Given lags and general random time delays on the web, you don't expect any server pages to be loaded instantly, so you tell the web-driver to always wait 10 seconds for result before timing out. You can do whatever you wish with the result of your search query. In this case, the HTML fragment ```h3>div``` which starts the "Show More" clickable tag on the search results page. Running this code with ```python example.py``` will result, via the final line ```print(first_result.get_attribute("textContent"))``` with the text ```Show More``` in your terminal. Congratulations: you just did an automated Google search and fished something out of the search results.

## Automating: the hard part

Let's go a step further, and have Selenium click on the "Next" link, to take us to the 2nd page of search results.  To do this, you'll have to fish through the search page's html code and try to figure out how the "Next" link works.

What I did is to download the "developer edition" of the Firefox browser. It has a "web inspector" which you can find here

![Alt text](Images/001_inspector.png?raw=true)

This in a nutshell, is what you do with Selenium: direct it to load pages from the web, then look for things of interest to you in the text of web-pages read back into variables, then act on them. This means fill in text-boxes, click on links, etc.
