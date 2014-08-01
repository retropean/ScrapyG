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
		
		#select the region
		region_counter = 1
		origin_counter = 1
		destination_counter = 1
		last_origin = 100
		last_destination = 100
		while (region_counter <= 5):
			while(origin_counter <= last_origin):
				while(destination_counter <= last_destination):
					self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listRegion_Input')))
					elem = self.driver.find_element_by_id("ctl00_body_listRegion_Input")
					elem.click()
					time.sleep(1)
					
					region_pattern = ".//div[@id='ctl00_body_listRegion_DropDown']/div/ul/li[{r_counter}]".format(r_counter = region_counter)
					elem = self.driver.find_element_by_xpath(region_pattern)
					region = self.driver.find_element_by_xpath(region_pattern).text
					elem.click()
					time.sleep(1)
				
					#select the origin
					elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listOrigin_Input')))
					elem = self.driver.find_element_by_id("ctl00_body_listOrigin_Input")
					elem.click()
					time.sleep(1)
					
					origin_pattern = ".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[{o_counter}]".format(o_counter = origin_counter)
					try:
						elem = self.driver.find_element_by_xpath(origin_pattern)
					except:
						origin_counter = 1
						destination_counter = 1
						region_counter = region_counter + 1
						break
					origin = (self.driver.find_element_by_xpath(origin_pattern).text)
					elem.click()
					time.sleep(1)
					
					#select the destination
					elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_Input')))
					elem = self.driver.find_element_by_id("ctl00_body_listDestination_Input")
					elem.click()
					time.sleep(1)
					
					destination_pattern = ".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[{d_counter}]".format(d_counter = destination_counter)
					try:
						elem = self.driver.find_element_by_xpath(destination_pattern)
					except:
						destination_counter = 1
						print "Finished scraping departures from origin " + origin
						break
					destination = (self.driver.find_element_by_xpath(destination_pattern).text)
					elem.click()
					time.sleep(1)
					
					#select the date
					elem = self.driver.find_element_by_id("ctl00_body_departureDate_dateInput_text")
					elem.click()
					elem.clear()
					elem.send_keys(fourteendate)
					elem.send_keys("\t")
					
					elem = self.driver.find_element_by_id("expHpBookingSearchTixBtn")
					elem.click()
					time.sleep(7)
					
					#begin to collect information
					print "Scraping " + origin + " to " + destination + " on " + fourteendate
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
					
					self.driver.back()
					destination_counter = destination_counter + 1
				origin_counter = origin_counter + 1
			region_counter = region_counter + 1
		return items