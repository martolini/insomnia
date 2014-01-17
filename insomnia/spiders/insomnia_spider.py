from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from datetime import datetime
from insomnia.items import InsomniaItem

class InsomniaSpider(BaseSpider):
	name = 'insomnia'
	allowed_domains = ['insomnia.gr']
	urls = []
	counter = 0


	def append_and_start_request(self):
		with open('urls.txt') as urlfile:
			for url in urlfile.readlines():
				if url not in self.urls:
					self.urls.append(url)
		if self.counter < len(self.urls):
			return Request(url=self.urls[self.counter], callback=self.parse_thread)
			self.counter += 1
		return None

	def start_requests(self):
		yield self.append_and_start_request()

	def parse_thread(self, response):
		hxs = HtmlXPathSelector(response)
		all_posts = hxs.select('//div[contains(@class,"post_block hentry clear clearfix")]')
		for num, post in enumerate(all_posts):
			post_id = post.select('@id').extract()[0].lstrip('post_id_')
			if post_id == u'':
				continue
			post_id = int(post_id)
			datestr =post.select('div/div/p/abbr/@title').extract()[0][0:10]
			date = datetime.strptime(datestr, '%Y-%m-%d')
			url = post.select('div/h3/span/a/@href').extract()[0]
			title = post.select('div/h3/span/a/@title').extract()[0]
			rawtext = post.select('div/div/div[@itemprop="commentText"]//text()').extract()
			text = ''.join(x for x in rawtext if x.strip())
			username = post.select('div/h3/span/a/span/text()').extract()[0]
			item = InsomniaItem()
			item['post_id'] = post_id
			item['date'] = date
			item['url'] = url
			item['title'] = title
			item['text'] = text
			item['username'] = username
			item['question'] = (num == 0)
			yield item

		next_page = hxs.select('//li[@class="next"]/a/@href').extract()
		if next_page:
			yield Request(url=next_page[0], callback=self.parse_thread)

		self.append_and_start_request()



