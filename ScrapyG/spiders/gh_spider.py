from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import Join, MapCompose

from ScrapyG.locations import alllocations
from ScrapyG.items import FareItem

from selenium import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import datetime
from datetime import timedelta

class GHSpider(Spider):
	name = "gh"
	custom_settings = {
		"DOWNLOAD_DELAY": 3,
		"RETRY_ENABLED": True,
	}
	allowed_domains = ["https://www.greyhound.com"]
	start_urls = ["https://www.greyhound.com/"]
	
	def __init__(self, daysoutcmmd=0, regioncounter=0, *args, **kwargs):
		#to switch back to firefox (for debugging) uncomment L25 & comment L27-28 or viceversa:
		self.driver = webdriver.Firefox()
		#self.driver = webdriver.PhantomJS()
		#self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
		#self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
		self.driver.set_window_size(1120, 1000)
		
		self.daysout = daysoutcmmd
		self.regioncount = regioncounter
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		CrawlSpider.__del__(self)

	def parse(self, response):
		locations = []
		locations = alllocations
		items = []
		
		for location in locations:
			try:
				self.driver.get("https://www.greyhound.com/")
				self.wait = WebDriverWait(self.driver, 100)
				print 'Top of the loop'
				scrapedate = datetime.datetime.now() + datetime.timedelta(int(self.daysout))
				year = str(scrapedate.year)
				day = scrapedate.strftime('%d')
				month = scrapedate.strftime('%m')
				readdate = month + '/' + day + '/' + year
				year=int(year)
				day=int(day)
				month=int(month)
				departdate=datetime.date(year, month, day)

				print response.request.headers['User-Agent']
				self.driver.save_screenshot("./test.png")
				
				print 'Enter origin ' + location[0]
				self.wait.until(EC.presence_of_element_located((By.ID, "fromLocation")))
				elem = self.driver.find_element_by_id("fromLocation")
				elem.click()
				elem.clear()
				elem.send_keys(location[0])
				self.wait.until(EC.presence_of_element_located((By.ID, 'fromStationHeader')))
				#try:
				#	self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
				#except:
				#	print("The origin "+location[0]+" is not included")
				#	continue
				time.sleep(3)
				elem.send_keys("\t")
				
				print 'Enter destination ' + location[1]
				elem = self.driver.find_element_by_id("toLocation")
				elem.click()
				elem.clear()
				elem.send_keys(location[1])
				self.wait.until(EC.presence_of_element_located((By.ID, 'toStationHeader')))
				#try:
				#	self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
				#except:
				#	print("The destination "+location[1]+" is not included")
				#	continue
				time.sleep(3)
				elem.send_keys("\t")
				
				print 'Enter date ' + readdate
				elem = self.driver.find_element_by_id("datepicker-from")
				elem.click()
				elem.clear()
				elem.send_keys(readdate)
				time.sleep(3)
				elem.send_keys("\t")
				time.sleep(3)
							
				elem = self.driver.find_element_by_id("fare-search-btn")
				elem.click()
				print 'Search for fares from ' + location[2] + ' to ' + location[3] + ' for ' + readdate + '.'
			
				self.wait.until(EC.presence_of_element_located((By.ID, 'schedule-calendar')))
			
				print 'Looking for fare calendar.'
				sites = self.driver.find_elements_by_xpath('//tr[@class="trip-details"]')
				time.sleep(5)
				print 'Scraping ' + location[2] + ' to ' + location[3] + ' for ' + readdate + '.'
				for site in sites:
					item = FareItem()
					
					item['stdfare'] = ((site.find_element_by_xpath(".//td[@class='trip-price trip-price-offline']").text)).rstrip("\n>")		
					print 'good stdfare'
					item['webfare'] = (site.find_element_by_xpath(".//td[@class='trip-price']").text)					
					print 'good webfare'
					item['origtime'] = ((site.find_element_by_xpath(".//li[@class='trip-from']/p[@class='trip-time trip-time-lg']").text)).rsplit('(', 1)[0]					
					print 'good otime'
					item['desttime'] = (((site.find_element_by_xpath(".//li[@class='trip-to']/p[@class='trip-time trip-time-lg']").text)).rsplit('(', 1)[0]).rstrip("\n")
					print 'good dtime'
					item['orig'] = str(location[2])
					item['dest'] = str(location[3])
					item['date'] = departdate
					
					#Clean the duration variable
					durfix = str(site.find_element_by_xpath(".//p[@class='trip-duration']").text)
					hour = durfix[0:durfix.index('h')]
					minutes = durfix[durfix.index('h')+2:durfix.index('m')]
					hour = int(hour)
					minutes = int(minutes)
					durfix = datetime.timedelta(hours=hour, minutes=minutes)
					print 'good triptime'
					item['duration'] = durfix
					item['transfers'] = int(site.find_element_by_xpath(".//p[@class='trip-transfers']").text[:1])
					print 'good transfers'
					item['timescraped'] = str(datetime.datetime.now().time())
					item['datescraped'] = str(datetime.datetime.now().date())
					
					#Check whether the fare is an Express bus
					try:
						site.find_element_by_xpath(".//li/span[@class='icon icn-006ecom-lrg icon-express']")
						item['express'] = "yes"
					except:
						item['express'] = "no"
					print 'good express'
					items.append(item)
					
			except:
				print 'Error, going back'
				self.driver.back()
			print 'All good, going back'		
			self.driver.back()
		return items