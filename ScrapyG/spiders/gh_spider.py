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
#from scrapy.contrib.loader.processor import Join, MapCompose

import time
import datetime

class GHSpider(CrawlSpider):
	name = "gh"
	download_delay = 5
	allowed_domains = ["https://www.greyhound.com/express/"]
	start_urls = ["https://www.greyhound.com/Express/WhereWeGo.aspx"]
	
	def __init__(self, daysoutcmmd=0, regioncounter=0, *args, **kwargs):
		#to switch back to firefox (for debugging) uncomment L25 & comment L27-28 or viceversa:
		#self.driver = webdriver.Firefox()
		self.driver = webdriver.PhantomJS()
		self.driver.set_window_size(1120, 550)
		CrawlSpider.__init__(self)
		self.daysout = daysoutcmmd
		self.regioncount = regioncounter
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		try:
			self.driver.get("https://www.greyhound.com/Express/WhereWeGo.aspx")
			self.wait = WebDriverWait(self.driver, 100)
			items = []
			
			#Set up the date to be scraped based on user input
			'''readdays = datetime.datetime.now() + datetime.timedelta(days=daysout)
			year = str(readdays.year)
			day = str(readdays.day)
			month = str(readdays.month)'''
			scrapedate = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
			year = str(scrapedate.year)
			day = scrapedate.strftime('%d')
			month = scrapedate.strftime('%m')
			readdate = month + '/' + day + '/' + year
			
			#select the region
			region_counter = int(self.regioncount)
			origin_counter = 1
			destination_counter = 1
			last_origin = 100
			last_destination = 100
			while (region_counter <= int(self.regioncount)):
				while(origin_counter <= last_origin):
					while(destination_counter <= last_destination):
						self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listRegion_Input')))
						elem = self.driver.find_element_by_id("ctl00_body_listRegion_Input")
						elem.click()
						time.sleep(3)
						
						region_pattern = ".//div[@id='ctl00_body_listRegion_DropDown']/div/ul/li[{r_counter}]".format(r_counter = region_counter)
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listRegion_DropDown')))
						elem = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='ctl00_body_listRegion_DropDown']/div/ul/li[1]")))
						elem = self.driver.find_element_by_xpath(region_pattern)
						region = self.driver.find_element_by_xpath(region_pattern).text
						elem.click()
						time.sleep(3)
					
						#select the origin
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listOrigin_Input')))
						elem = self.driver.find_element_by_id("ctl00_body_listOrigin_Input")
						elem.click()
						origin_pattern = ".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[{o_counter}]".format(o_counter = origin_counter)
						try:
							elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listOrigin_DropDown')))
							elem = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[1]")))
							time.sleep(3)
							elem = self.driver.find_element_by_xpath(origin_pattern)
						except:
							origin_counter = 1
							destination_counter = 1
							region_counter = region_counter + 1
							break
						origin = (self.driver.find_element_by_xpath(origin_pattern).text)
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listOrigin_DropDown')))
						elem = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='ctl00_body_listOrigin_DropDown']/div/ul/li[1]")))
						elem = self.driver.find_element_by_xpath(origin_pattern)
						elem.click()
						time.sleep(3)
						
						#select the destination
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_Input')))
						elem = self.driver.find_element_by_id("ctl00_body_listDestination_Input")
						elem.click()
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_DropDown')))
						time.sleep(3)
						destination_pattern = ".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[{d_counter}]".format(d_counter = destination_counter)
						try:
							elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_DropDown')))
							elem = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[1]")))
							time.sleep(3)
							elem = self.driver.find_element_by_xpath(destination_pattern)
						except:
							destination_counter = 1
							print "Finished scraping departures from origin " + origin
							break
						destination = (self.driver.find_element_by_xpath(destination_pattern).text)
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_listDestination_DropDown')))
						elem = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@id='ctl00_body_listDestination_DropDown']/div/ul/li[1]")))
						elem = self.driver.find_element_by_xpath(destination_pattern)
						elem.click()
						time.sleep(3)
						
						if origin == destination:
							print "Origin and destination are the same."
							destination_counter = destination_counter + 1
							continue
						
						#select the date
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_departingDate_dateInput_text')))
						elem = self.driver.find_element_by_id("ctl00_body_departingDate_dateInput_text")
						elem.click()
						elem.clear()
						elem.send_keys(readdate)
						elem.send_keys("\t")
						
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'expWwgSelectBookNowBtn')))
						elem = self.driver.find_element_by_id("expWwgSelectBookNowBtn")
						elem.click()
						time.sleep(7)
						elem = self.wait.until(EC.presence_of_element_located((By.ID, 'modifySearchLink_new')))
						
						#begin to collect information
						print "Scraping " + origin + " to " + destination + " on " + readdate
						sites = self.driver.find_elements_by_xpath('//tr[@class="innerRow"]')

						for site in sites:
							item = FareItem()
							item['stdfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f3 fareS']").text)
							item['advfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f2 fareS']").text)
							item['webfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f1 fareS']").text)
							item['reffare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f4 fareS']").text)
							item['origtime'] = (site.find_element_by_xpath(".//td[@class='ptStep2departCol']").text).split("\n",1)[0]
							item['desttime'] = (site.find_element_by_xpath(".//td[@class='ptStep2arriveCol']").text).split("\n",1)[0]
							item['region'] = region
							item['orig'] = origin
							item['dest'] = destination
							item['date'] = readdate
							item['duration'] = (site.find_element_by_xpath(".//td[@class='ptStep2travelTimeCol']").text)
							item['transfers'] = (site.find_element_by_xpath(".//td[@class='ptStep2transfersCol']").text)
							item['timescraped'] = str(datetime.datetime.now().time())
							item['datescraped'] = str(datetime.datetime.now().date())
							try:
								site.find_element_by_xpath(".//td[@class='ptStep2travelTimeCol']/img")
								item['express'] = "yes"
							except:
								item['express'] = "no"
							items.append(item)
						
						self.driver.back()
						destination_counter = destination_counter + 1
					origin_counter = origin_counter + 1
				region_counter = region_counter + 1
			return items
		except:
			return items