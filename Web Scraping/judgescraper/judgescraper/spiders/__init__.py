# Goal: scrape judge name from this url: http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi 
#for years 2005-2019 using Wayback Machine archives
# outputs csv of all judges (and clerks and chieg magistrates) from 2005 to 2019

import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	start_urls = ["http://web.archive.org/web/20050616025741/http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi"]

	def parse(self, response):
		year = response.css("td.c")[2].attrib["title"][-4:]
		for row in response.css("table.people tr"):
			letters = row.css("td")[0].css("b::text").extract()
			name = ""
			name = name.join(letters)
			try:
				court = row.css("td")[1].css("::text").extract()[0]
			except IndexError:
				court = "Unknown"
			yield {
				"Judge": name,
				"Year": year,
				"Court": court
			}


		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse)


# response.css("table.people tr")[1].css("td")[1].css("::text").extract()
