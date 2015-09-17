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
	allowed_domains = ["https://www.greyhound.com"]
	start_urls = ["https://www.greyhound.com/"]
	
	def __init__(self, daysoutcmmd=0, regioncounter=0, *args, **kwargs):
		#to switch back to firefox (for debugging) uncomment L25 & comment L27-28 or viceversa:
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.PhantomJS()
		#self.driver.set_window_size(1120, 550)
		CrawlSpider.__init__(self)
		self.daysout = daysoutcmmd
		self.regioncount = regioncounter
		
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		locations = (["Washington, DC","Chicago, IL"],["Chicago, IL","Washington, DC"],["Chicago, IL","Los Angeles, CA"])
		items = []
		for location in locations:
			self.driver.get("https://www.greyhound.com/")
			self.wait = WebDriverWait(self.driver, 100)
			
			#Set up the date to be scraped based on user input
			scrapedate = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
			year = str(scrapedate.year)
			day = scrapedate.strftime('%d')
			month = scrapedate.strftime('%m')
			readdate = month + '/' + day + '/' + year
			
			#Enter origin
			self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_search_listOrigin_Input')))
			elem = self.driver.find_element_by_id("ctl00_body_search_listOrigin_Input")
			elem.click()
			elem.send_keys(location[0])
			time.sleep(1)
			elem.send_keys("\t")
			
			#Enter destination
			elem = self.driver.find_element_by_id("ctl00_body_search_listDestination_Input")
			elem.click()
			elem.send_keys(location[1])
			time.sleep(1)
			elem.send_keys("\t")
			
			#Enter date
			elem = self.driver.find_element_by_id("ctl00_body_search_dateDepart_dateInput_text")
			elem.click()
			elem.clear()
			elem.send_keys(readdate)
			elem.send_keys("\t")
						
			elem = self.driver.find_element_by_id("ticketsSearchSchedules")
			elem.click()
			
			self.wait.until(EC.presence_of_element_located((By.ID, 'departPreviousDayImage')))
			sites = self.driver.find_elements_by_xpath('//tr[@class="innerRow"]')
			for site in sites:
				item = FareItem()
				item['stdfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f3 fareS']").text)
				item['advfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f2 fareS']").text)
				item['webfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f1 fareS']").text)
				item['reffare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f4 fareS']").text)
				item['origtime'] = (site.find_element_by_xpath(".//td[@class='ptStep2departCol']").text).split("\n",1)[0]
				item['desttime'] = (site.find_element_by_xpath(".//td[@class='ptStep2arriveCol']").text).split("\n",1)[0]
				item['orig'] = location[0]
				item['dest'] = location[1]
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
		return items