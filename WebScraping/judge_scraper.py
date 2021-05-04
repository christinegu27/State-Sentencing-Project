# Goal: scrape judge name from this url: http://web.archive.org/web/20050616025741/http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi
# outputs csv of all judges (and clerks and chieg magistrates)

import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	start_urls = ["http://web.archive.org/web/20050616025741/http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi"]

	def parse(self, response):
		for row in response.css("table.people tr"):
			letters = row.css("td")[0].css("b::text").extract()
			name = ""
			name = name.join(letters)
			year = response.css("td.c")[2].attrib["title"][-4:]

			yield {
				"Judge": name
				# "Year": year
			}


		next_page = response.css("td.f a")[2].attrib["href"]

		if next_page is not None:
			url = next_page
			yield scrapy.Request(url, callback = self.parse)