"""
Get a list of clickable elements by xpath
using expected conditions
We use the Hoyts movie chain site (without permission) to test
You can find the documentation for waits here:
https://selenium-python.readthedocs.io/waits.html

This is a complex xpath which requires us to check whether
certain conditions are true

We collect the links for every movie currently showing and pickle
Then in a file called href_list.pickle
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


browser.maximize_window() #makes it easier to see what is going on

#Will wait for up to 30 secs when using expected conditions
#In reality you rpbioably want this to be < 10 seconds
wait = WebDriverWait(browser, 30) 

BF = BrowserFuncs(browser, EC, By, datetime) #see browserfuncs file

GF = GenFuncs(pickle, os, datetime, sys)

#In this example we are going to collect a list of 
#links associated with movies from the Hoyts movie website
#we are going to save the result in a pickle file



xpath = '//div[contains(@class, "movie-list-item")]'
xpath+= '//div[contains(@class, "item-header-container")]'
# we need to check that the movie name is not blank
xpath+= '//span[contains(@class, "item-header") and text() != ""]' 
# Now go back up the tree
xpath+= '//ancestor::div[contains(@class, "movie-list-item")]' 
xpath+= '//div[contains(@class, "item-info-container")]//a'
print('xpath= $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ')

print(xpath)

print('')

#Allow up to ten tries
#Probably would not want that many in an operational program
max_tries = 10
href_list = []
url = 'https://www.hoyts.com.au/movies'
browser.get(url)

for try_nbr in range(max_tries):
	print('try_nbr= ' + str(try_nbr))
	try:
		elem_list = BF.get_list_by_xpath_with_exp_cond(xpath, wait)
		for elem in elem_list:
			href_list.append(elem.get_attribute('href'))
		break
	except Exception as e:
		print('get elem list failed')
		print(type(e))
		print(e.args)
		print(e)
		if try_nbr >= max_tries - 1:
			print('Maxed out tries')
			browser.quit()
			sys.exit()
		else:
			browser.refresh()


browser.quit()



#we now pickle the list of hrefs
#datfiles is a subdirectory os this one
fname = 'datfiles/href_list.pickle'
max_tries = 4

GF.write_to_pickle(fname, href_list, max_tries)

# Just to prove it worked we'll read href_list back from pickle file
#re-initialise href_list

href_list = []
max_tries = 4
fname = 'datfiles/href_list.pickle'

href_list = GF.read_from_pickle(fname, max_tries)

i = 0
for h in href_list:
	print(str(i) + ' ' + h)
	print('')
	i+= 1

	






