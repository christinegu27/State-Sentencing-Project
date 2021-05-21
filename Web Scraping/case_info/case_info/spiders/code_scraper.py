import scrapy
from scrapy.shell import inspect_response

class code_scraper(scrapy.Spider):
	name = "codes"

	start_urls = ["https://eapps.courts.state.va.us/ocis-rest/api/public/getCourtsCodeDetails"]

	def parse(self, response):
		yield scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCourtsCodeDetails",
			callback = self.code_details)

	def code_details(self, response):
		code_details = response.json()['context']['entity']['payload']
		for codes in code_details:
			try:
				codes['description']
			except KeyError:
				codes['description'] = "No description" 


			yield{
				'Court Category': codes['courtCategory'],
				'Code ID': codes['codeId'],
				'Code Description': codes['description'],
				'Code Type': codes['codeType'],
				}			

class court_codes(scrapy.Spider):
	name = "court_codes"

	start_urls = ["https://eapps.courts.state.va.us/ocis-rest/api/public/getLookupCodeDetails"]

	def parse(self, response):
		court_details = response.json()['context']['entity']['payload']['allCourts']
		for court in court_details:
			yield{
				'Court Name': court['courtName'],
				'Court ID': court['fipsCode4']
				}		
