class BrowserFuncs():
	def __init__(self, browser, EC, By, datetime):
		self.browser = browser
		self.EC = EC
		self.By = By
		self.datetime = datetime

	def get_list_by_xpath_with_exp_cond(self, xpath, wait):
		#Get element list using using xpath and expected condtions
		EC = self.EC
		By = self.By
		elem_list = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
		return elem_list

	
	def get_elem_by_css_simple(self, selector, wait):
		"""
		We have two versions of this. One is simple with no try - except
		The other, below, has a try - except
		I found it useful to have both versions
		"""
		
		browser = self.browser
		EC = self.EC
		By = self.By
		elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
		return elem
		
	
	def get_elem_by_css(self, selector, wait_time, max_tries):
		"""
		get element by CSS selector
		As only one element put try/except in function
		but also have simpliefied version withg no try-except
		See above
		"""
		browser = self.browser
		browser.implicitly_wait(wait_time)
		for try_nbr in range(max_tries):
			try:
				print('try_nbr: ' + str(try_nbr))
				elem = browser.find_element_by_css_selector(selector)
				break
			except Exception as e:
				print(type(e))
				print(e.args)
				print(e)
				elem = 'BUMMER'
		return elem
		

		
		
		
	def get_click_elem_by_css(self, selector, wait):
		EC = self.EC
		By = self.By
		elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
		return elem
			
	def get_click_elem_by_xpath(self, xpath, wait):
		EC = self.EC
		By = self.By
		elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
		return elem
		
	def get_list_by_xpath(self, xpath, wait_time):
		self.browser.implicitly_wait(wait_time)
		elem_list = self.browser.find_elements_by_xpath(xpath)
		return elem_list
		
	def get_elem_by_xpath(self, xpath, wait):
		EC = self.EC
		By = self.By
		elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
		return elem

		






	
