import scrapy

class JudgeSpider(scrapy.Spider):
	name = "accomack"
	start_urls = ["https://web.archive.org/web/20050409104858/http://www.courts.state.va.us/courts/circuit/Accomack/home.html"]

	def parse(self, response):
		year = response.css("td.c")[2].attrib["title"][-4:]
		for judge in response.css("li.judges").css("::text").extract():
			yield {
				"Judge": judge,
				"Year":year
			}

		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse)

