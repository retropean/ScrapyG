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
		locations = (["Washington, DC","Chicago, IL"],["Chicago, IL","San Francisco, CA"],["Chicago, IL","Washington, DC"],["Chicago, IL","Los Angeles, CA"],["Los Angeles, CA","Chicago, IL"],["Chicago, IL","Seattle, WA"],["Chicago, IL","Denver, CO"],["San Francisco, CA","Chicago, IL"],["New York, NY","Chicago, IL"],["Seattle, WA","Chicago, IL"],["Chicago, IL","New York, NY"],["Los Angeles, CA","Seattle, WA"],["Denver, CO","Chicago, IL"],["Sacramento, CA","Chicago, IL"],["Chicago, IL","Portland, OR"],["Seattle, WA","Los Angeles, CA"],["New York, NY","Orlando, FL"],["Atlanta, GA","New York, NY"],["New York, NY","Atlanta, GA"],["New Orleans, LA","Chicago, IL"],["Chicago, IL","Sacramento, CA"],["Chicago, IL","Albany, NY"],["Chicago, IL","New Orleans, LA"],["Chicago, IL","Flagstaff, AZ"],["Chicago, IL","Pittsburgh, PA"],["Portland, OR","Chicago, IL"],["New York, NY","Richmond, VA"],["Albany, NY","Chicago, IL"],["Orlando, FL","New York, NY"],["Albuquerque, NM","Los Angeles, CA"],["Los Angeles, CA","Portland, OR"],["Pittsburgh, PA","Chicago, IL"],["Chicago, IL","Kansas City, MO"],["Kansas City, MO","Chicago, IL"],["Los Angeles, CA","Albuquerque, NM"],["Chicago, IL","Whitefish (e), MT"],["Chicago, IL","Salt Lake City, UT"],["Memphis, TN","New Orleans, LA"],["Los Angeles, CA","New Orleans, LA"],["Denver, CO","San Francisco, CA"],["Chicago, IL","Memphis, TN"],["Flagstaff, AZ","Chicago, IL"],["New Orleans, LA","Memphis, TN"],["Memphis, TN","Chicago, IL"],["New Orleans, LA","Los Angeles, CA"],["Chicago, IL","St Paul, MN"],["Seattle, WA","San Francisco, CA"],["Richmond, VA","New York, NY"],["Dallas, TX","Chicago, IL"],["Chicago, IL","Albuquerque, NM"],["Chicago, IL","Buffalo, NY"],["Albuquerque, NM","Chicago, IL"],["Chicago, IL","Dallas, TX"],["San Francisco, CA","Denver, CO"],["Chicago, IL","Jackson, MS"],["San Francisco, CA","Seattle, WA"],["Jackson, MS","Chicago, IL"],["Seattle, WA","Sacramento, CA"],["St Paul, MN","Chicago, IL"],["Washington, DC","Orlando, FL"],["Atlanta, GA","Washington, DC"],["Los Angeles, CA","Oakland, CA"],["San Antonio, TX","Chicago, IL"],["Chicago, IL","St Louis, MO"],["Orlando, FL","Washington, DC"],["Portland, OR","Los Angeles, CA"],["Syracuse, NY","Chicago, IL"],["Chicago, IL","Syracuse, NY"],["New Orleans, LA","New York, NY"],["Longview, TX","Chicago, IL"],["Flagstaff, AZ","Los Angeles, CA"],["Charleston, SC","New York, NY"],["Jacksonville, FL","New York, NY"],["Chicago, IL","Longview, TX"],["New Orleans, LA","Birmingham, AL"],["Buffalo, NY","Chicago, IL"],["Salt Lake City, UT","Chicago, IL"],["Sacramento, CA","Denver, CO"],["St Paul, MN","Seattle, WA"],["Sacramento, CA","Seattle, WA"],["Portland, OR","Sacramento, CA"],["New York, NY","Charleston, SC"],["Chicago, IL","San Antonio, TX"],["St Louis, MO","Chicago, IL"],["Washington, DC","Atlanta, GA"],["Denver, CO","Sacramento, CA"],["Chicago, IL","Raton, NM"],["Kansas City, MO","Los Angeles, CA"],["New York, NY","New Orleans, LA"],["New York, NY","Raleigh, NC"],["Grand Junction, CO","Chicago, IL"],["New York, NY","Jacksonville, FL"],["New York, NY","Miami, FL"],["Los Angeles, CA","Kansas City, MO"],["Seattle, WA","St Paul, MN"],["Fayetteville, NC","New York, NY"],["Birmingham, AL","New Orleans, LA"],["Charlotte, NC","New York, NY"],["Houston, TX","Los Angeles, CA"],["Reno, NV","Chicago, IL"],["Philadelphia, PA","Orlando, FL"],["Florence, SC","New York, NY"],["Miami, FL","New York, NY"],["Chicago, IL","Reno, NV"],["Washington, DC","New Orleans, LA"],["New York, NY","Florence, SC"],["New York, NY","Charlotte, NC"],["Raleigh, NC","New York, NY"],["Los Angeles, CA","Eugene, OR"],["New York, NY","Charlottesville, VA"],["Oakland, CA","Los Angeles, CA"],["Los Angeles, CA","San Antonio, TX"],["San Antonio, TX","Los Angeles, CA"],["New York, NY","Fayetteville, NC"],["Charlottesville, VA","New York, NY"],["Chicago, IL","Cleveland, OH"],["New York, NY","Rocky Mount, NC"],["San Francisco, CA","Portland, OR"],["Rocky Mount, NC","New York, NY"],["Seattle, WA","Portland, OR"],["Whitefish (e), MT","Chicago, IL"],["Cleveland, OH","Chicago, IL"],["Sacramento, CA","Portland, OR"],["Portland, OR","San Francisco, CA"],["Orlando, FL","Philadelphia, PA"],["Chicago, IL","Rochester, NY"],["New Orleans, LA","Washington, DC"],["Portland, OR","St Paul, MN"],["New York, NY","Kissimmee, FL"],["Boston, MA","Chicago, IL"],["Los Angeles, CA","Houston, TX"],["Tucson, AZ","Los Angeles, CA"],["Atlanta, GA","Philadelphia, PA"],["Washington, DC","Raleigh, NC"],["Toledo, OH","Washington, DC"],["Spokane, WA","Chicago, IL"],["Philadelphia, PA","Atlanta, GA"],["Los Angeles, CA","San Jose, CA"],["Los Angeles, CA","Flagstaff, AZ"],["Austin, TX","Chicago, IL"],["Chicago, IL","Glenwood Springs (e), CO"],["Fort Worth, TX","Chicago, IL"],["Chicago, IL","Fort Worth, TX"],["New York, NY","Tampa, FL"],["Chicago, IL","Spokane, WA"],["Tampa, FL","New York, NY"],["Rochester, NY","Chicago, IL"],["New York, NY","Wilson, NC"],["St Paul, MN","Portland, OR"],["Savannah, GA","New York, NY"],["Wilson, NC","New York, NY"],["Chicago, IL","Austin, TX"],["Raleigh, NC","Washington, DC"],["New York, NY","Savannah, GA"],["Washington, DC","Savannah, GA"],["Denver, CO","Glenwood Springs (e), CO"],["Raton, NM","Chicago, IL"],["Greensboro, NC","New York, NY"],["West Palm Beach, FL","New York, NY"],["Jacksonville, FL","Washington, DC"],["Charlotte, NC","Raleigh, NC"],["New Orleans, LA","Atlanta, GA"],["Washington, DC","Toledo, OH"],["Kingman, AZ","Chicago, IL"],["Richmond, VA","Washington, DC"],["Little Rock, AR","Chicago, IL"],["Philadelphia, PA","Richmond, VA"],["Raleigh, NC","Charlotte, NC"],["Atlanta, GA","Newark, NJ"],["Chicago, IL","Little Rock, AR"],["Washington, DC","Jacksonville, FL"],["Birmingham, AL","New York, NY"],["Atlanta, GA","New Orleans, LA"],["Chicago, IL","Grand Junction, CO"],["Savannah, GA","Washington, DC"],["Chicago, IL","Omaha, NE"],["New York, NY","Birmingham, AL"],["Chicago, IL","Greenwood, MS"],["Kissimmee, FL","New York, NY"],["Fort Lauderdale, FL","New York, NY"],["Chicago, IL","Boston, MA"],["Charleston, SC","Washington, DC"],["Toledo, OH","Chicago, IL"],["Seattle, WA","Whitefish (e), MT"],["Salt Lake City, UT","Sacramento, CA"],["Charlotte, NC","Washington, DC"],["Chicago, IL","Kingman, AZ"],["Washington, DC","Charlotte, NC"],["San Jose, CA","Los Angeles, CA"],["Washington, DC","Charleston, SC"],["Salt Lake City, UT","San Francisco, CA"],["Chicago, IL","Toledo, OH"],["Galesburg, IL","Denver, CO"],["New York, NY","Greensboro, NC"],["Newark, NJ","Atlanta, GA"],["New York, NY","West Palm Beach, FL"],["Sacramento, CA","Salt Lake City, UT"],["San Jose, CA","Seattle, WA"],["Portland, OR","Seattle, WA"],["Glenwood Springs (e), CO","Denver, CO"],["Los Angeles, CA","Tucson, AZ"],["New York, NY","Syracuse, NY"],["New York, NY","Fort Lauderdale, FL"],["Denver, CO","Galesburg, IL"],["Kansas City, MO","Raton, NM"],["Oakland, CA","Seattle, WA"],["New York, NY","Toledo, OH"],["Omaha, NE","Chicago, IL"],["Richmond, VA","Philadelphia, PA"],["St Paul, MN","Whitefish (e), MT"],["New York, NY","Columbia, SC"],["Washington, DC","Richmond, VA"],["Eugene, OR","Sacramento, CA"],["New York, NY","Rochester, NY"],["Chicago, IL","Williston, ND"],["San Bernardino, CA","Chicago, IL"],["San Jose, CA","Portland, OR"],["Washington, DC","Greensboro, NC"],["Chicago, IL","La Crosse, WI"],["Fayetteville, NC","Washington, DC"],["Williston, ND","Spokane, WA"],["Denver, CO","Salt Lake City, UT"],["Milwaukee, WI","Seattle, WA"],["Washington, DC","Fayetteville, NC"],["Los Angeles, CA","Raton, NM"],["Los Angeles, CA","Tacoma, WA"],["Washington, DC","Pittsburgh, PA"],["Greensboro, NC","Washington, DC"],["Denver, CO","Grand Junction, CO"],["Newark, NJ","Orlando, FL"],["Seattle, WA","San Jose, CA"],["Columbia, SC","New York, NY"],["Spokane, WA","Williston, ND"],["Raleigh, NC","Philadelphia, PA"],["Chicago, IL","Fargo, ND"],["Portland, OR","Whitefish (e), MT"],["Chicago, IL","Minot, ND"],["Chicago, IL","Champaign, IL"],["Philadelphia, PA","Raleigh, NC"],["New York, NY","Cleveland, OH"],["New Orleans, LA","Jackson, MS"],["Williston, ND","Chicago, IL"],["Jackson, MS","New Orleans, LA"],["Washington, DC","Rocky Mount, NC"],["Richmond, VA","Charleston, SC"],["Florence, SC","Washington, DC"],["Charlotte, NC","Newark, NJ"],["Washington, DC","Florence, SC"],["Tampa, FL","Miami, FL"],["Whitefish (e), MT","Seattle, WA"],["Glenwood Springs (e), CO","Chicago, IL"],["Toledo, OH","New York, NY"],["Durham, NC","Charlotte, NC"],["Washington, DC","Miami, FL"],["New York, NY","Buffalo, NY"],["Tacoma, WA","Sacramento, CA"],["Rocky Mount, NC","Washington, DC"],["Cleveland, OH","New York, NY"],["Oakland, CA","Portland, OR"],["Denver, CO","Reno, NV"],["Los Angeles, CA","Fort Worth, TX"],["Miami, FL","Tampa, FL"],["Charleston, SC","Richmond, VA"],["Philadelphia, PA","Jacksonville, FL"],["Los Angeles, CA","San Luis Obispo (e), CA"],["Portland, OR","San Jose, CA"],["Newark, NJ","Florence, SC"],["Kansas City, MO","Flagstaff, AZ"],["Washington, DC","Wilson, NC"],["Seattle, WA","Oakland, CA"],["Carbondale (e), IL","Chicago, IL"],["Jacksonville, FL","Philadelphia, PA"],["Los Angeles, CA","Dallas, TX"],["Charleston, SC","Philadelphia, PA"],["Chicago, IL","Galesburg, IL"],["Chicago, IL","Sandusky, OH"],["Buffalo, NY","New York, NY"],["Chicago, IL","Erie, PA"],["Florence, SC","Newark, NJ"],["Newark, NJ","Charlotte, NC"],["Charlotte, NC","Durham, NC"],["Portland, OR","Spokane, WA"],["Miami, FL","Washington, DC"],["Newton (e), KS","Chicago, IL"],["Denver, CO","Omaha, NE"],["Spokane, WA","Portland, OR"],["Grand Junction, CO","Denver, CO"],["Temple, TX","Chicago, IL"],["Rochester, NY","New York, NY"],["Tampa, FL","West Palm Beach, FL"],["Fort Worth, TX","Los Angeles, CA"],["West Palm Beach, FL","Tampa, FL"],["Philadelphia, PA","Florence, SC"],["San Francisco, CA","Salt Lake City, UT"],["Philadelphia, PA","Charleston, SC"],["Wilson, NC","Washington, DC"],["Chicago, IL","Waterloo, IN"],["Los Angeles, CA","Little Rock, AR"],["Eugene, OR","Los Angeles, CA"],["La Crosse, WI","Chicago, IL"],["Seattle, WA","Milwaukee, WI"],["Minot, ND","Chicago, IL"],["Champaign, IL","Chicago, IL"],["Orlando, FL","Newark, NJ"],["Whitefish (e), MT","St Paul, MN"],["Chicago, IL","Carbondale (e), IL"],["Florence, SC","Philadelphia, PA"],["Raton, NM","Kansas City, MO"],["Philadelphia, PA","Tampa, FL"],["Pittsburgh, PA","Washington, DC"],["Everett, WA","Chicago, IL"],["Sacramento, CA","Eugene, OR"],["Charlotte, NC","Philadelphia, PA"],["Chicago, IL","Newton (e), KS"],["Williston, ND","St Paul, MN"],["Schenectady, NY","Chicago, IL"],["Newark, NJ","Raleigh, NC"],["New York, NY","Utica, NY"],["Chicago, IL","Winona St Univ (e), MN"],["Fayetteville, NC","Philadelphia, PA"],["Los Angeles, CA","Sacramento, CA"],["Durham, NC","New York, NY"],["Chicago, IL","Everett, WA"],["Omaha, NE","Denver, CO"],["Sacramento, CA","Los Angeles, CA"],["Philadelphia, PA","Fayetteville, NC"],["Minot, ND","St Paul, MN"],["Philadelphia, PA","Savannah, GA"],["Savannah, GA","Philadelphia, PA"],["Philadelphia, PA","Charlotte, NC"],["Dallas, TX","Los Angeles, CA"],["St Paul, MN","Williston, ND"],["Birmingham, AL","Newark, NJ"],["New York, NY","Durham, NC"],["San Francisco, CA","Reno, NV"],["Tacoma, WA","Los Angeles, CA"],["San Antonio, TX","Fort Worth, TX"],["Kansas City, MO","Albuquerque, NM"],["Winona St Univ (e), MN","Chicago, IL"],["St Paul, MN","Minot, ND"],["Whitefish (e), MT","Portland, OR"],["Seattle, WA","Spokane, WA"],["Longview, TX","St Louis, MO"],["Los Angeles, CA","Salinas, CA"],["Richmond, VA","Orlando, FL"],["Erie, PA","Chicago, IL"],["Tampa, FL","Philadelphia, PA"],["Raleigh, NC","Newark, NJ"],["Cleveland, OH","Washington, DC"],["Sacramento, CA","Tacoma, WA"],["Raleigh, NC","Orlando, FL"],["Los Angeles, CA","San Francisco, CA"],["Waterloo, IN","Chicago, IL"],["Chicago, IL","Springfield, IL"],["Fayetteville, NC","Newark, NJ"],["Raton, NM","Los Angeles, CA"],["Newark, NJ","Fayetteville, NC"],["Tucson, AZ","Chicago, IL"],["Albany, NY","Boston, MA"],["Riverside, CA","Chicago, IL"],["El Paso, TX","Los Angeles, CA"],["Fort Worth, TX","San Antonio, TX"],["Reno, NV","Denver, CO"],["Washington, DC","Tampa, FL"],["Sacramento, CA","Reno, NV"],["Newark, NJ","Birmingham, AL"],["Boston, MA","Albany, NY"],["Portland, OR","Oakland, CA"],["Chicago, IL","Temple, TX"],["Portland, OR","Minot, ND"],["San Francisco, CA","Los Angeles, CA"],["Richmond, VA","Wilmington, DE"],["Greenville, SC","New York, NY"],["Minot, ND","Portland, OR"],["Charleston, SC","Orlando, FL"],["Omaha, NE","Sacramento, CA"],["Fargo, ND","Chicago, IL"],["New York, NY","Kingstree, SC"],["New York, NY","Greenville, SC"],["Chicago, IL","San Bernardino, CA"],["Albuquerque, NM","Kansas City, MO"],["Chicago, IL","Tucson, AZ"],["Seattle, WA","Minot, ND"],["Birmingham, AL","Washington, DC"],["Dallas, TX","St Louis, MO"],["Denver, CO","Osceola, IA"],["Tampa, FL","Washington, DC"],["Chicago, IL","Charlottesville, VA"],["Washington, DC","South Bend, IN"],["Newark, NJ","Richmond, VA"],["Spokane, WA","Seattle, WA"],["Portland, OR","Pasco, WA"],["San Luis Obispo (e), CA","Seattle, WA"],["Flagstaff, AZ","Kansas City, MO"],["Chicago, IL","Bloomington Normal, IL"],["Orlando, FL","Raleigh, NC"],["St Louis, MO","Longview, TX"],["Washington, DC","Cleveland, OH"],["Philadelphia, PA","Wilson, NC"],["Cincinnati, OH","Chicago, IL"],["Seattle, WA","Eugene, OR"],["Williston, ND","Portland, OR"],["Chicago, IL","Lincoln, NE"],["Orlando, FL","Charleston, SC"],["Seattle, WA","Williston, ND"],["Philadelphia, PA","Chicago, IL"],["Chicago, IL","Riverside, CA"],["Portland, OR","Williston, ND"],["San Francisco, CA","Grand Junction, CO"],["Newark, NJ","Rocky Mount, NC"],["Minot, ND","Seattle, WA"],["Lynchburg (e), VA","New York, NY"],["Los Angeles, CA","Galesburg, IL"],["Galesburg, IL","Los Angeles, CA"],["Wilmington, DE","Richmond, VA"],["Chicago, IL","Schenectady, NY"],["Gallup, NM","Los Angeles, CA"],["Los Angeles, CA","Newton (e), KS"],["New York, NY","Tuscaloosa, AL"],["New York, NY","Lynchburg (e), VA"],["Champaign, IL","New Orleans, LA"],["St Louis, MO","Dallas, TX"],["Rocky Mount, NC","Newark, NJ"],["Salt Lake City, UT","Denver, CO"],["Fort Lauderdale, FL","Tampa, FL"],["Milwaukee, WI","St Paul, MN"],["Lincoln, NE","Reno, NV"],["Philadelphia, PA","New Orleans, LA"],["Richmond, VA","Newark, NJ"],["Naperville (e), IL","Denver, CO"],["Wilson, NC","Newark, NJ"],["Utica, NY","Chicago, IL"],["Omaha, NE","Reno, NV"],["Austin, TX","Los Angeles, CA"],["Los Angeles, CA","El Paso, TX"],["Portland, OR","Milwaukee, WI"],["Orlando, FL","Richmond, VA"],["Washington, DC","Birmingham, AL"],["South Bend, IN","Washington, DC"],["Osceola, IA","Denver, CO"],["New York, NY","Albany, NY"],["New Orleans, LA","Philadelphia, PA"],["Philadelphia, PA","Rocky Mount, NC"],["Chicago, IL","Wisconsin Dells, WI"],["Martinsburg, WV","Chicago, IL"],["Oakland, CA","Santa Barbara, CA"],["Washington, DC","Kissimmee, FL"],["Richmond, VA","Savannah, GA"])
		
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
			self.wait.until(EC.presence_of_element_located((By.ID, 'ctl00_body_search_listOrigin_Input')))
			elem = self.driver.find_element_by_id("ctl00_body_search_listOrigin_Input")
			elem.click()
			elem.send_keys(location[0])
			time.sleep(1)
			try:
				self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
			except:
				print("The origin "+location[0]+" is not included")
				continue
			time.sleep(.5)
			elem.send_keys("\t")
			
			#Enter destination
			elem = self.driver.find_element_by_id("ctl00_body_search_listDestination_Input")
			elem.click()
			elem.send_keys(location[1])
			time.sleep(1)
			try:
				self.driver.find_element_by_xpath("//li[@class='rcbHovered']").click()
			except:
				print("The destination "+location[1]+" is not included")
				continue
			time.sleep(.5)
			elem.send_keys("\t")
			
			#Enter date
			elem = self.driver.find_element_by_id("ctl00_body_search_dateDepart_dateInput_text")
			elem.click()
			elem.clear()
			elem.send_keys(readdate)
			elem.send_keys("\t")
						
			elem = self.driver.find_element_by_id("ticketsSearchSchedules")
			elem.click()

			self.wait.until(EC.presence_of_element_located((By.ID, 'modifySearchLink_new')))
			print 'Scraping ' + location[0] + ' to ' + location[1] + ' for ' + readdate + '.'
			sites = self.driver.find_elements_by_xpath('//tr[@class="innerRow"]')
			try:
				for site in sites:
					item = FareItem()
					item['stdfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f3 fareS']").text)
					item['advfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f2 fareS']").text)
					item['webfare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f1 fareS']").text)
					item['reffare'] = (site.find_element_by_xpath(".//td[@class='ptStep2f4 fareS']").text)
					item['origtime'] = (site.find_element_by_xpath(".//td[@class='ptStep2departCol']").text).split("\n",1)[0]
					item['desttime'] = (site.find_element_by_xpath(".//td[@class='ptStep2arriveCol']").text).split("\n",1)[0]
					item['orig'] = str(location[0])
					item['dest'] = str(location[1])
					item['date'] = departdate
					
					#clean the duration variable
					durfix = str(site.find_element_by_xpath(".//td[@class='ptStep2travelTimeCol']").text)
					hour = durfix[0:durfix.index('H')]
					minutes = durfix[durfix.index('H')+2:durfix.index('M')]
					hour = int(hour)
					minutes = int(minutes)
					durfix = datetime.time(hour, minutes)
					item['duration'] = durfix					
					item['transfers'] = int(site.find_element_by_xpath(".//td[@class='ptStep2transfersCol']").text)
					item['timescraped'] = str(datetime.datetime.now().time())
					item['datescraped'] = str(datetime.datetime.now().date())
					try:
						site.find_element_by_xpath(".//td[@class='ptStep2travelTimeCol']/img")
						item['express'] = "yes"
					except:
						item['express'] = "no"
					items.append(item)
			except:
				print 'No fares or other error'
				continue
			self.driver.back()
		return items