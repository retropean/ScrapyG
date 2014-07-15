# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScrapygItem(Item):
    # define the fields for your item here like:
    # name = Field()
	stdfare = Field()
	reffare = Field()
	advfare = Field()
	webfare = Field()
	duration = Field()
	origtime = Field()
	desttime = Field()
	transfers = Field()
	orig = Field()
	dest = Field()
	date = Field()
	timescraped = Field()
	datescraped = Field()
pass