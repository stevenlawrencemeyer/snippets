"""

We iterate through every movie collecting the names
of the cinemas in the state of Victoria
Where they are playing
We put them in a dictionary and pickle


"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import sys
import time
import pickle
import os

#modules is a subdirectory of this directory
#BrowserFuncs is a class that contains functions using webdriver
from modules.browserfuncs import BrowserFuncs
#GenFuncs is a class containing functions that do not use a webdriver
from modules.genfuncs import GenFuncs

#We use chrome
browser = webdriver.Chrome() 
print(dir(browser))

browser.maximize_window() #makes it easier to see what is going on

#Will wait for up to 30 secs when using expected conditions
#In reality you probably want this to be < 10 seconds
wait = WebDriverWait(browser, 5) 

BF = BrowserFuncs(browser, EC, By, datetime) #see browserfuncs file
GF = GenFuncs(pickle, os, datetime, sys)

#Will explain this later
cleansed_allowed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


#get list of movie links from previous program
fname = 'datfiles/href_list.pickle'

wait_time = 4
max_tries = 4
movie_links = GF.read_from_pickle(fname, max_tries) 

#We will use this later to get movie name
selector = 'div[class="banner-container"] '
selector+= 'div[class="hero"] '
selector+= 'h2[class*="text"]'

#We will use this later to expose movie houses
xpath1 = '//div[contains(@class, "container") and contains(@class, "body-content")]'
xpath1+= '//div[contains(@class, "top")]'
xpath1+= '//button[contains(@class, "add") and contains(@class, "red")]'
xpath1+= '//i[contains(@class, "sprite")]'

#We will use this to expose VIC movie houses
xpath2 = '//div[contains(@class, "row") and contains(@class, "states")]'
xpath2+= '//a[contains(@class, "state") and text() = "VIC"]'

#We will use this to get list of VIC movie houses
#Where movie is playing (There may be none in VIC)

#We will use this to get list of VIC movie houses
#Where movie is playing (There may be none in VIC)
xpath3 = '//div[contains(@class, "row") and contains(@class, "cinemas")]'
#exclude elements where the class contains "off-opacity"
xpath3+= '//div[contains(@class, "cinema-selector") and not(contains(@class, "off-opacity"))]'
xpath3+= '//a//span[contains(@class, "text")]'







movie_nbr = 0
movie_max_tries = 4

movie_dict_list = []


for mlink in movie_links:
	print('movie_nbr= ' + str(movie_nbr))

	print(mlink)
	browser.get(mlink)

	for movie_tries in range(movie_max_tries):
		print('movie_tries= ' + str(movie_tries))
		try:
			#get movie name from file created in previous program
			elem = BF.get_elem_by_css_simple(selector, wait)
			movie_name = elem.text
			movie_key = GF.cleanse_str(cleansed_allowed, movie_name)
			dict1 = {'movie_name':movie_name, 'movie_key':movie_key, 
			'movie_link':mlink}
			#now expose movie houses
			click_plus = BF.get_click_elem_by_xpath(xpath1, wait)
			click_plus.click()
			# find "VIC" movie houses
			vic_btn = BF.get_click_elem_by_xpath(xpath2, wait)
			vic_btn.click()
			#NB We cannot use expected conditions because we do not know
			#whether a particular movie is playing in any Victorian movie house
			#it may be plainging in none
			#So, instead we get the list with an implict wait
			elem_list = BF.get_list_by_xpath(xpath3, wait_time)
			print(movie_name)
			list1 = []
			for elem in elem_list:
				list1.append(elem.text)
		
			dict1['movie_houses'] = list1
			movie_dict_list.append(dict1)
			movie_nbr+= 1
			break
		except Exception as e:
			print(type(e))
			print(e.args)
			print(e)
			browser.refresh()
		if movie_tries >= movie_max_tries - 1:
			print('You maxed out your tries')
			browser.quit()
			sys.exit()

print('iteration done')
browser.quit()


#Pickle movie_dict_list
fname = 'datfiles/movie_dict.pickle'
max_tries = 4
GF.write_to_pickle(fname, movie_dict_list, max_tries)

#Read movie_dict_list back

movie_dict_list = {}

movie_dict_list = GF.read_from_pickle(fname, max_tries)

print('')
print('MOVIE DICT LIST')
print('')

for m in movie_dict_list:
	print(m['movie_name'])
	print(m['movie_key'])
	print(m['movie_link'])
	for mh in m['movie_houses']:
		print('    ' + mh)
	print('')
	


