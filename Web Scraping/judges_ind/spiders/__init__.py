# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	start_urls = ["https://web.archive.org/web/20050901023917/http://www.courts.state.va.us/courts/circuit.html"]

	def parse(self, response):
	    for href in response.xpath("//li//@href").extract():
	    	if href[:5]=='/web/':
	        	url = "https://web.archive.org"+href
	        	yield scrapy.Request(url, callback = self.parse_dir_contents)


	def parse_dir_contents(self, response):
		year = response.css("td.c")[2].attrib["title"][-4:]
		court = response.xpath('//h1').extract()[0].split("\n")[1].strip()

		# post 2005 website
		for judge in response.css("li.judges").css("::text").extract():
			yield {
				"Judge": judge,
				"Year":year,
				"Court": court
			}

		# # pre 2005 website
		# for row in response.xpath('//*[@width = "170"]//td[@width="164"]//text()').extract():
		# 	if "Hon" in row:
		# 		judge = row[3:-2]
		# 		yield {
		# 			"Court": self.court,
		# 			"Judge":judge
		# 			}

		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse_dir_contents)