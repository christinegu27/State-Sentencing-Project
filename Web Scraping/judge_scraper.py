# Goal: scrape judge name from this url: http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi
# outputs csv of all judges (and clerks and chieg magistrates)

import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges"
	start_urls = ["http://webdev.courts.state.va.us/cgi-bin/p/peoplesearch.cgi"]

	def parse(self, response):
		for row in response.css("table.people tr"):
			letters = row.css("td")[0].css("b::text").extract()
			name = ""
			name = name.join(letters)

			yield {
				"Judge": name
			}


			