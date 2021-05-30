import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	start_urls = ["https://web.archive.org/web/20050318043738/http://www.courts.state.va.us:80/courts/circuit.html"]

	def parse(self, response):
		#get list of links from circuit court homepage
	    for href in response.xpath("//li//@href").extract():
	    	if href[:5]=='/web/': #excludes certain links that are unecessary
	        	url = "https://web.archive.org"+href
	        	yield scrapy.Request(url, callback = self.parse_base)


	def parse_base(self, response): #starts at individual court home page
		#going back on wayback machine
		prev_page = response.xpath('//*[@class = "d"]//td[@class = "b"]//a/@href').extract_first()
		if prev_page:
			yield scrapy.Request(prev_page, callback = self.parse_old_contents)

		#going forward on wayback machine
		next_page = response.css("td.f a")[2].attrib["href"]
		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse_new_contents)

	
	def parse_new_contents(self, response): #gets judges from new version of website
		#gets year and court name
		year = response.css("td.c")[2].attrib["title"][-4:]
		try:
			court = response.xpath('//h1').extract()[0].split("\n")[1].strip()
		except IndexError: #wrong website format, skip page
			pass 

		for judge in response.css("li.judges").css("::text").extract():
			yield {
				"Judge": judge,
				"Year":year,
				"Court": court
			}

		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page:
			yield scrapy.Request(next_page, callback = self.parse_new_contents)
		
	def parse_old_contents(self,response): #gets judges from old version of website
		#gets year and court name
		year = response.css("td.c")[2].attrib["title"][-4:]

		try:
			court = response.xpath('//*[@valign = "middle"]//font[@size = "6"]//text()').extract_first()
			court = court[1:-1] #remove \n at beginning and end
		except: #wrong website format, skip page
			pass

		for row in response.xpath('//*[@width = "170"]//td[@width="164"]//text()').extract():
			if "Hon" in row: #only gets rows with judge names
				judge = row[3:-2]
				yield {
					"Judge":judge,
					"Year":year,
					"Court": court
					}

		prev_page = response.xpath('//*[@class = "d"]//td[@class = "b"]//a/@href').extract_first()

		if prev_page:
			yield scrapy.Request(prev_page, callback = self.parse_old_contents)

