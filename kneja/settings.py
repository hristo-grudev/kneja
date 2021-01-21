BOT_NAME = 'kneja'

SPIDER_MODULES = ['kneja.spiders']
NEWSPIDER_MODULE = 'kneja.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'kneja.pipelines.KnejaPipeline': 100,

}