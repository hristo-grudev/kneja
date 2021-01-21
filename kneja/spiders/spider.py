import re
import scrapy

from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from ..items import KnejaItem


class KnejaSpider(scrapy.Spider):
	name = 'kneja'
	start_urls = ['https://kneja.acstre.com/section-156-content.html']
	page = 1

	def parse(self, response):
		posts = response.xpath('//div[@class=" col-xs-12" or @class="col-lg-9 col-xs-12"]')
		for post in posts:
			url = post.xpath('.//div[@class="new-item-caption"]/a/@href').get()
			date = post.xpath('.//div[@class="new-date-text"]/span/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs=dict(date=date))

		self.page += 1
		next_page = f'section-156-{self.page}.html'

		if not posts:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)

	def parse_post(self, response, date):
		print(response)
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="new-item-content"]').getall()
		if description:
			comments = re.sub(r'<!--[\S\s]*?-->', '', str(description[0]))
			description = remove_tags(str(comments)).strip()
		else:
			description = ''

		item = ItemLoader(item=KnejaItem(), response=response)
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date.strip())

		return item.load_item()
