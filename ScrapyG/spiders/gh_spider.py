from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.selector import Selector

from ScrapyG.items import FareItem

from selenium import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime

class BBSpider(CrawlSpider):
	name = "gh"
	download_delay = 5
	allowed_domains = ["https://www.greyhound.com/express/"]
	start_urls = ["https://www.greyhound.com/express/"]
	
	def __init__(self):
		self.driver = webdriver.Firefox()
		CrawlSpider.__init__(self)
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		self.driver.get("https://www.greyhound.com/express/")
		self.wait = WebDriverWait(self.driver, 20)
		items = []
		
		#find date to scrape that is fourteen days out
		fourteendays = datetime.datetime.now() + datetime.timedelta(days=14)
		year = str(fourteendays.year)
		day = str(fourteendays.day)
		month = str(fourteendays.month)
		fourteendate = month + '/' + day + '/' + year

		#add all locations
		#locations = (["Midwest", "Ann Arbor", "Chicago"], ["Midwest", "Ann Arbor", "Detroit"], ["Midwest", "Buffalo", "Chicago"], ["Midwest", "Buffalo", "Cincinnati"], ["Midwest", "Buffalo", "Cleveland"], 
		#["Midwest", "Buffalo", "Columbus"], ["Midwest", "Buffalo", "Detroit"], ["Midwest", "Buffalo", "Erie"], ["Midwest", "Buffalo", "Toledo"], 
		#["Midwest", "Buffalo", "Chicago"], ["Midwest", "Champaign", "Atlanta"], ["Midwest", "Champaign", "Chicago"], ["Midwest", "Champaign", "Chicago 95th & Dan Ryan"], ["Midwest", "Champaign", "Effingham"], ["Midwest", "Champaign", "Memphis"], ["Midwest", "Champaign", "Milwaukee"], ["Midwest", "Champaign", "St Louis"], 
		#["Midwest", "Chicago", "Ann Arbor"], ["Midwest", "Chicago", "Atlanta"], ["Midwest", "Chicago", "Buffalo"], ["Midwest", "Chicago", "Champaign"], ["Midwest", "Chicago", "Chattanooga"], ["Midwest", "Chicago", "Cincinnati"], ["Midwest", "Chicago", "Cleveland"], ["Midwest", "Chicago", "Dallas"], ["Midwest", "Chicago", "Davenport"], ["Midwest", "Chicago", "Des Moines"], ["Midwest", "Chicago", "Detroit"], ["Midwest", "Chicago", "Effingham"], ["Midwest", "Chicago", "Erie"],
		#["Midwest", "Chicago", "Indianapolis"], ["Midwest", "Chicago", "Iowa City"], ["Midwest", "Chicago", "Lafayette (e)"], ["Midwest", "Chicago", "Little Rock"], ["Midwest", "Chicago", "London"], ["Midwest", "Chicago", "Louisville"],  ["Midwest", "Chicago", "Macon"], ["Midwest", "Chicago", "Memphis"], ["Midwest", "Chicago", "Milwaukee"], ["Midwest", "Chicago", "Minneapolis"], ["Midwest", "Chicago", "Nashville"], ["Midwest", "Chicago", "New York"], ["Midwest", "Chicago", "Newark"], ["Midwest", "Chicago", "Savannah"], 
		#["Midwest", "Chicago", "St Louis"], ["Midwest", "Chicago", "Texarkana"], ["Midwest", "Chicago", "Toledo"], ["Midwest", "Chicago", "Toronto"], ["Midwest", "Chicago", "Windsor"], 
		#)
		
		#select the region
		#print "Scraping " + str(locations[1]) + " to " + str(locations[2]) + " on " + fourteendate
		region_counter = 1
		while (region_counter <= 5):
			self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listRegion_Input')))
			elem = self.driver.find_element_by_id("ctl00_body_listRegion_Input")
			elem.click()
			time.sleep(1)
			
			#elem = self.driver.find_element_by_xpath(".//li[contains(., locations[0])]")
			region_pattern = ".//div[@id='ctl00_body_listRegion_DropDown']/div/ul/li[{r_counter}]".format(r_counter = region_counter)
			elem = self.driver.find_element_by_xpath(region_pattern)
			region = self.driver.find_element_by_xpath(region_pattern).text
			elem.click()
			
			#select the origin
			time.sleep(1)
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listOrigin_Input')))
			elem = self.driver.find_element_by_id("ctl00_body_listOrigin_Input")
			elem.click()
			time.sleep(1)
					
			origin = (self.driver.find_element_by_xpath(".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[1]").text)
			elem = self.driver.find_element_by_xpath(".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[1]")
			
			elem.click()
			
			#select the destination
			time.sleep(1)
			elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_Input')))
			elem = self.driver.find_element_by_id("ctl00_body_listDestination_Input")
			elem.click()
			time.sleep(1)
			
			destination = (self.driver.find_element_by_xpath(".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[1]").text)
			elem = self.driver.find_element_by_xpath(".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[1]")
			elem.click()
			
			#select the date
			time.sleep(1)
			elem = self.driver.find_element_by_id("ctl00_body_departureDate_dateInput_text")
			elem.click()
			elem.clear()
			elem.send_keys(fourteendate)
			elem.send_keys("\t")
			
			elem = self.driver.find_element_by_id("expHpBookingSearchTixBtn")
			elem.click()
			
			time.sleep(7)
			#begin to collect information
			sites = self.driver.find_elements_by_xpath('//tr[@class="innerRow"]')

			for site in sites:
				item = FareItem()
				item['stdfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f3 fareS']").text)
				item['advfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f2 fareS']").text)
				item['webfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f1 fareS']").text)
				item['reffare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f4 fareS']").text)
				item['origtime'] = (site.find_element_by_xpath(".//td[@class='ptStep2departCol']").text)
				item['desttime'] = (site.find_element_by_xpath(".//td[@class='ptStep2arriveCol']").text)
				item['region'] = region
				item['orig'] = origin
				item['dest'] = destination
				item['date'] = fourteendate
				item['duration'] = (site.find_element_by_xpath(".//td[@class='ptStep2travelTimeCol']").text)
				item['transfers'] = (site.find_element_by_xpath(".//td[@class='ptStep2transfersCol']").text)
				item['timescraped'] = str(datetime.datetime.now().time())
				item['datescraped'] = str(datetime.datetime.now().date())
				items.append(item)
			region_counter = region_counter + 1
			self.driver.back()
		return items