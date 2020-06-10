#!python
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
import sys



def send_delayed_keys(element, text, delay=0.1):
    for c in text :
        element.send_keys(c)
        time.sleep(delay)

def wait_for_by_id(elem_id):
	print "waiting for id "+elem_id
	try:
		elem = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, elem_id)))
	except:
		print "could not find "+elem_id+". Please click on it."
		x=raw_input("Press [Return] when done...")
		elem = False

	return(elem)

def wait_for_by_link_text(elem_id):
	print "waiting for link " + elem_id
	elem = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, elem_id)))
	return(elem)
	
def wait_for_by_class_name(elem_id):
	print "waiting for class name "+elem_id
	elem = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, elem_id)))
	return(elem)

def wait_for_by_xpath(xpath):
	print "waiting for xpath "+xpath
	try:
		elem = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
	except:
		print "could not find "+xpath+". Please click on it."
		x=raw_input("Press [Return] when done...")
		elem = False

	return(elem)


def fill_in_by_id(elem_id,text):
	elem = wait_for_by_id(elem_id)
	elem.clear()
	elem.send_keys(text)
	elem.send_keys(Keys.TAB)
	time.sleep(0.5)

def click_on_by_id(elem_id):
	elem = wait_for_by_id(elem_id)
	if elem != False:
		elem.click()

def click_on_by_link_text(elem_id):
	elem = wait_for_by_link_text(elem_id)
	elem.click()

def click_on_by_xpath(xpath):
	elem = wait_for_by_xpath(xpath)
	if elem != False:
		elem.click()

def select_dropdown_by_id(elem_id,value):
	elem = wait_for_by_id(elem_id)
	for option in elem.find_elements_by_tag_name("option"):
		if option.text == value:
			option.click()
			time.sleep(1)
			break
	wait_for_spinner()


def get_classes_in_ps():
	#https://sqa.stackexchange.com/questions/18354/how-to-identify-element-with-knowledge-of-partial-text-for-any-tag-eg-div-span
	#https://sqa.stackexchange.com/questions/10342/how-to-find-element-using-contains-in-xpath
	try:
		elem = browser.find_element_by_xpath('//span[starts-with(text(), "1-")]')
	except: 
		return([])

	parts = elem.text.split(" ")
	class_count = parts[2]
	classes_found = []

	for i in range(int(class_count)):
		id = "RESULT3$" + str(i)
		elem = browser.find_element_by_id(id)
		classes_found.append(str(elem.text).strip())

	return(classes_found)


def enter_class_info(section_number,assoc_number,type,enroll_type,print_yn,room,days,start,end,ecap,emplid,topic,notenbr):
	time.sleep(1)
	click_on_by_id("ICTAB_0")
	time.sleep(1)
	wait_for_spinner()

	fill_in_by_id("CLASS_TBL_CLASS_SECTION$0",section_number.rjust(2,'0'))
	wait_for_spinner()
	
	#PS Quirk..won't accept class type without a save now

	click_save_button()

	if topic:
		fill_in_by_id("CLASS_TBL_CRS_TOPIC_ID$67$$0",topic)
		wait_for_spinner()


	fill_in_by_id("CLASS_TBL_SSR_COMPONENT$0",type)
	wait_for_spinner()

	if enroll_type == 'N':
		select_dropdown_by_id("CLASS_TBL_CLASS_TYPE$0","Non-Enrollment Section")
		wait_for_spinner()
	
	if print_yn == 'N':
		click_on_by_id("CLASS_TBL_SCHEDULE_PRINT$0")
		wait_for_spinner()

	fill_in_by_id("CLASS_TBL_ASSOCIATED_CLASS$0",assoc_number.rjust(2,'0'))
	wait_for_spinner();

	click_on_by_id("ICTAB_1")
	time.sleep(1)
	wait_for_spinner()

	if room:
		fill_in_by_id("CLASS_MTG_PAT_FACILITY_ID$0",room)
		wait_for_spinner()

	if days:
		fill_in_by_id("CLASS_MTG_PAT_STND_MTG_PAT$0",days)
		wait_for_spinner()

	if start:
		fill_in_by_id("CLASS_MTG_PAT_MEETING_TIME_START$0",start)
		wait_for_spinner()

	if end:
		fill_in_by_id("CLASS_MTG_PAT_MEETING_TIME_END$0",end)
		wait_for_spinner()

	if emplid:
		fill_in_by_id("CLASS_INSTR_EMPLID$0",emplid)
		wait_for_spinner()

	select_dropdown_by_id("CLASS_INSTR_GRADE_RSTR_ACCESS$0","Approve")
	wait_for_spinner()


	click_on_by_id("ICTAB_2")
	time.sleep(1)
	wait_for_spinner()

	fill_in_by_id("CLASS_TBL_ENRL_CAP$0",ecap)
	wait_for_spinner()
	fill_in_by_id("CLASS_TBL_ROOM_CAP_REQUEST$0",ecap)
	wait_for_spinner()
	fill_in_by_id("CLASS_TBL_WAIT_CAP$0","99")
	wait_for_spinner()

	if notenbr:
		click_on_by_id("ICTAB_4")
		time.sleep(1)
		wait_for_spinner()

		fill_in_by_id("CLASS_NOTES_CLASS_NOTE_NBR$0",notenbr)
		wait_for_spinner()

	click_on_by_id("ICTAB_0")
	time.sleep(1)
	wait_for_spinner()


def add_class(term_code,prefix,number):
	print "Adding " + prefix + "-" + number
	fill_in_by_id("CRSE_OFFER_SCTY_STRM",term_code)
	wait_for_spinner()
	
	fill_in_by_id("CRSE_OFFER_SCTY_SUBJECT",prefix)
	wait_for_spinner()
	fill_in_by_id("CRSE_OFFER_SCTY_CATALOG_NBR",number)
	wait_for_spinner()
	fill_in_by_id("CRSE_OFFER_SCTY_CRSE_ID","")
	wait_for_spinner()
	click_on_by_id('#ICSearch')


def choose_favorite(fav):
	browser.refresh()
	click_on_by_xpath('//*[@id="pthnavbc_MYFAVORITES"]')
	if fav == 'maintain':
		click_on_by_xpath('/html/body/div[3]/div/header/div[1]/div[1]/nav/div[1]/ul/li[1]/div/div[2]/div[2]/ul/li[1]/ul/li[5]/a')
	elif fav == 'new':
		click_on_by_xpath('/html/body/div[3]/div/header/div[1]/div[1]/nav/div[1]/ul/li[1]/div/div[2]/div[2]/ul/li[1]/ul/li[2]/a')
	else: print fav+' is not handled in favorites menu.'
	
	iframe = browser.find_element_by_id('ptifrmtgtframe')
	browser.switch_to.frame(iframe)

def maintain_search_for_class(term_code,class_prefix,class_number):
	wait_for_by_id('CLASS_TBL_SCTY_STRM')
	wait_for_by_id('#ICSearch')

	elem = browser.find_element_by_id("CLASS_TBL_SCTY_STRM")
	elem.send_keys(term_code)

	elem = browser.find_element_by_id("CLASS_TBL_SCTY_SUBJECT")
	elem.send_keys(class_prefix)

	elem = browser.find_element_by_id("CLASS_TBL_SCTY_CATALOG_NBR")
	elem.send_keys(class_number)

	elem = browser.find_element_by_id("#ICSearch")
	elem.click()

	if not class_number:
		try:
			wait_for_by_id('RESULT3$0')
		except:
			return

def maintain_remove_all_class(term_code,class_prefix,class_number):
	choose_favorite('maintain')
	maintain_search_for_class(term_code,class_prefix,class_number)

	wait_for_by_class_name('PSGRIDCOUNTER')

	elem = browser.find_element_by_class_name("PSGRIDCOUNTER")
	parts = elem.text.split(' ')

	for i in range(int(parts[2])):
		click_on_by_xpath('//*[@id="$ICField21$delete$0$$0"]')
		wait_for_spinner()
		browser.switch_to.default_content()
	    
		click_on_by_xpath('//*[@id="#ALERTOK"]')
		time.sleep(1)
		wait_for_spinner()

		iframe = browser.find_element_by_id('ptifrmtgtframe')
		browser.switch_to.frame(iframe)
		time.sleep(1)

	click_save_button()
	click_return_to_search()

def wait_for_spinner():
	LONG_TIMEOUT = 30  # give enough time for loading to finish

	time.sleep(1)
	LOADING_ELEMENT_XPATH = "//*[@id='SAVED_win0']"
	print "waiting for spinner"
	WebDriverWait(browser, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))

	LOADING_ELEMENT_XPATH = "//*[@id='WAIT_win0']"
	WebDriverWait(browser, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
	print "spinner done"


#https://stackoverflow.com/questions/26086965/wait-until-loader-disappears-python-selenium
def click_save_button():
	SHORT_TIMEOUT  = 5   # give enough time for the loading element to appear
	LONG_TIMEOUT = 30  # give enough time for loading to finish
	LOADING_ELEMENT_XPATH = "//*[@id='ptStatusText_win0']"
	click_on_by_id("#ICSave")
	time.sleep(1)
	wait_for_spinner()

	

#https://stackoverflow.com/questions/27003423/staleelementreferenceexception-on-python-selenium
def click_return_to_search():
	click_on_by_id("#ICList")

def delete_empty_class_form():
	click_on_by_xpath('//*[@id="$ICField21$delete$0$$0"]')
	wait_for_spinner()
	
	browser.switch_to.default_content()
	click_on_by_xpath('//*[@id="#ALERTOK"]')
	
	iframe = browser.find_element_by_id('ptifrmtgtframe')
	browser.switch_to.frame(iframe)


def click_popup_save_button():
	click_on_by_ud('ptpopupmsgbtn2')

#https://stackoverflow.com/questions/14158868/python-skip-comment-lines-marked-with-in-csv-dictreader
def csv_fill(file_name,class_prefix,class_number):
	with open(file_name) as csv_file:
	    the_file = csv.DictReader(csv_file, delimiter=',')
	    for row in the_file:
	    	if row['class'].lower() == (class_prefix + '-' + class_number).lower():
	    		enter_class_info(row['section_number'],row['assoc_number'],row['type'],row['enroll'],row['print'],row['room'],row['days'],row['start'],row['end'],row['ecap'],row['emplid'],row['topic'],row['notenbr'])
	    		time.sleep(1)
	    		click_on_by_id('$ICField21$new$0$$0')
	    		time.sleep(1)
	    		wait_for_spinner()

	time.sleep(2) #wait for new form to load.
	delete_empty_class_form() #get rid of it
	time.sleep(2)

def put_in_new_class(term_code,class_prefix,class_number,filename):
	print "Adding class: " + class_prefix + "-" + class_number
	choose_favorite('new')
	add_class(term_code,class_prefix,class_number)
	csv_fill(filename,class_prefix,class_number)
	click_save_button()
	time.sleep(5) # wait for save spinner
	click_return_to_search()


def csv_get_course_numbers(file_name,class_prefix):
	nums = []
	with open(file_name) as csv_file:
	    the_file = csv.DictReader(csv_file, delimiter=',')
	    for row in the_file:
	    	parts = row['class'].split('-')
	    	if parts[0].lower() == class_prefix.lower():
	    		nums.append(parts[1])
	#https://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
	return(list(set(nums)))


def remove_and_add(term_code,class_prefix,class_num,csv_file):
	print "Removing: "+class_prefix + "-" + class_num
	maintain_remove_all_class(term_code,class_prefix,class_num)
	time.sleep(2)

	put_in_new_class(term_code,class_prefix,class_num,csv_file)

##########################
term_code = '2212'
class_prefix = 'ASTR'
the_file = '2020Winter/project_classes.csv'
##########################

if len(sys.argv) != 3:
	print "Usage: psgo username password"
	exit()

username = sys.argv[1]
password = sys.argv[2]

unique_course_nums = csv_get_course_numbers(the_file,class_prefix)
print unique_course_nums

start = time.time()
browser = webdriver.Chrome('/path/to/chrome-driver')
#browser = webdriver.Safari()
#browser.maximize_window()
browser.get('https://your-enterprise-address')
handle0 = browser.current_window_handle
print handle0

fill_in_by_id('username',username)
time.sleep(1)
fill_in_by_id("password",password)
time.sleep(1)

elem = browser.find_element_by_name("_eventId_proceed")
elem.click();

click_on_by_xpath('//*[@id="tabLink_u21l1s5"]')
click_on_by_xpath('/html/body/div/div/div[3]/div/div/div[5]/div[2]/div/div[2]/div/div[3]/div/div[1]/h2[1]/a')
time.sleep(1)


print browser.window_handles

for h in browser.window_handles:
	if h <> handle0:
		browser.switch_to.window(h)
		print h


#get all classes currenlty in ps
classes_in_ps = []


# choose_favorite('maintain')
# maintain_search_for_class(term_code,class_prefix,'')
# classes_in_ps = get_classes_in_ps()
# print classes_in_ps

# #first, remove all classes currently in PS
# for class_num in classes_in_ps:
# 	print "Removing: "+class_prefix + "-" + class_num
# 	maintain_remove_all_class(term_code,class_prefix,class_num)
# 	time.sleep(2)

# #now, put in all classes called for in csv file
# for class_num in unique_course_nums:
# 	if class_num not in classes_in_ps:
# 		print "Adding: "+class_prefix + "-" + class_num
# 		put_in_new_class(term_code,class_prefix,class_num,the_file)
# 		time.sleep(2)

#one off
#put_in_new_class(term_code,'GEOL','415',the_file)

#some that are already deleted
# for num in ['141','121','122','123','132','133']:
# 	put_in_new_class(term_code,'PHYS',num,the_file)
#remove_and_add(term_code,'PHYS','133',the_file)
#put_in_new_class(term_code,'ASTR','101',the_file)

for num in ['461','462']:
	remove_and_add(term_code,'PHYS',num,the_file)


#for num in ['200','400','461','462']:
 #	remove_and_add(term_code,classes_in_ps,'PHYS',num,the_file)

# astr project classes

#for num in ['200','400']:
#	remove_and_add(term_code,'ASTR',num,the_file)

#for num in ['200','400']:
#	remove_and_add(term_code,'GEOL',num,the_file)

#put_in_new_class(term_code,'GEOL','400',the_file)

#for num in ['200','400']:
#	remove_and_add(term_code,'PHYS',num,the_file)

#remove_and_add(term_code,'PHYS','462',the_file)
#
# for num in ['200','400']:
# 	put_in_new_class(term_code,'ASTR',num,the_file)

# for num in ['101','102','326','444']:
# 	put_in_new_class(term_code,'ASTR',num,the_file)

#put_in_new_class(term_code,'ASTR','444',the_file)

# for num in ['101','201','391','424','491']:
#  	remove_and_add(term_code,'PSC',num,the_file)

#put_in_new_class(term_code,'PSC','424',the_file)

#remove_and_add(term_code,'PHYS','408',the_file)

end = time.time()
print "ran for "+str(end-start) + " seconds or " + str((end-start)/60)+" minutes."


