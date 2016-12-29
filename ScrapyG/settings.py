from credentials import ur, pw

BOT_NAME = 'ScrapyG'
ROBOTSTXT_OBEY = False

SPIDER_MODULES = ['ScrapyG.spiders']
NEWSPIDER_MODULE = 'ScrapyG.spiders'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

DATABASE = {
	'drivername': 'postgres',
	'host': 'localhost',
	'port': '5432',
	'username': ur,
	'password': pw,
	'database': 'scrapyg'
}

ITEM_PIPELINES = {
    'ScrapyG.pipelines.GhPipeline': 300,
}