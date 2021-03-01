import scrapy

from scrapy.loader import ItemLoader
from ..items import Bank2noItem
from itemloaders.processors import TakeFirst


class Bank2noSpider(scrapy.Spider):
	name = 'bank2no'
	start_urls = ['https://bank2.no/blogg']

	def parse(self, response):
		post_links = response.xpath('//div[@class="et_pb_image_container"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="nextpostslink"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=Bank2noItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
