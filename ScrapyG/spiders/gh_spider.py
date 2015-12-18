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
		locations = (["Fresno","Modesto"],["Fresno","Stockton"])
		
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
			year=int(year)
			day=int(day)
			month=int(month)
			departdate=datetime.date(year, month, day)
			
			#Enter origin
			self.wait.until(EC.presence_of_element_located((By.ID, 'fromLocation')))
			elem = self.driver.find_element_by_id("fromLocation")
			elem.click()
			elem.send_keys(location[0])
			#try:
			#	self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
			#except:
			#	print("The origin "+location[0]+" is not included")
			#	continue
			time.sleep(3)
			elem.send_keys("\t")
			
			#Enter destination
			elem = self.driver.find_element_by_id("toLocation")
			elem.click()
			elem.send_keys(location[1])
			#try:
			#	self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
			#except:
			#	print("The destination "+location[1]+" is not included")
			#	continue
			time.sleep(3)
			elem.send_keys("\t")
			
			#Enter date
			elem = self.driver.find_element_by_id("datepicker-from")
			elem.click()
			elem.clear()
			elem.send_keys(readdate)
			time.sleep(3)
			elem.send_keys("\t")
			time.sleep(3)
						
			elem = self.driver.find_element_by_id("fare-search-btn")
			elem.click()

			self.wait.until(EC.presence_of_element_located((By.ID, 'schedule-calendar')))
			print 'Scraping ' + location[0] + ' to ' + location[1] + ' for ' + readdate + '.'
			sites = self.driver.find_elements_by_xpath('//tr[@class="fare-row"]')
			try:
				for site in sites:
					item = FareItem()
					item['stdfare'] = (site.find_element_by_xpath(".//td[@class='trip-price trip-price-offline']").text)
					#item['advfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f2 fareS']").text)
					item['webfare'] = (site.find_element_by_xpath(".//td[@class='trip-price']").text)
					#item['reffare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f4 fareS']").text)
					item['origtime'] = (site.find_element_by_xpath(".//td[@class='trip-time trip-time-small']").text)
					item['desttime'] = (site.find_element_by_xpath(".//td[@class='trip-time trip-time-small']").text)
					item['orig'] = str(location[0])
					item['dest'] = str(location[1])
					item['date'] = departdate
					
					#clean the duration variable
					durfix = str(site.find_element_by_xpath(".//td[@class='trip-duration']").text)
					hour = durfix[0:durfix.index('h')]
					minutes = durfix[durfix.index('h')+2:durfix.index('m')]
					hour = int(hour)
					minutes = int(minutes)
					durfix = datetime.time(hour, minutes)
					item['duration'] = durfix					
					item['transfers'] = int(site.find_element_by_xpath(".//td[@class='ptStep2transfersCol']").text)
					item['timescraped'] = str(datetime.datetime.now().time())
					item['datescraped'] = str(datetime.datetime.now().date())
					try:
						site.find_element_by_xpath(".//td[@class='trip-duration']")
						item['express'] = "yes"
					except:
						item['express'] = "no"
					items.append(item)
			except:
				print 'No fares or other error'
				continue
			self.driver.back()
		return items