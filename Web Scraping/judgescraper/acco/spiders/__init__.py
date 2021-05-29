import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	def __init__(self, court_url):
		super(scrapy.Spider, self)__init()
		self.court_url = court_url

	start_urls = [f"https://web.archive.org/web/20050313093326/http://www.courts.state.va.us:80/courts/circuit/{self.court_url}/home.html"]

	def parse(self, response):
		year = response.css("td.c")[2].attrib["title"][-4:]

		# post 2005 website
		for judge in response.css("li.judges").css("::text").extract():
			yield {
				"Judge": judge,
				"Year":year
			}

		# pre 2005 website
		for row in response.xpath('//*[@width = "170"]//td[@width="164"]//text()').extract():
			if "Hon" in row:
				judge = row[3:-2]
				yield {
					"Court": self.court,
					"Judge":judge
					}

		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse)

