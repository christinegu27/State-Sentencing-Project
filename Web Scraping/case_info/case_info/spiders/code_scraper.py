import scrapy

class code_scraper(scrapy.Spider):
	#codes used in the JSON for each case's details
	name = "codes"

	start_urls = ["https://eapps.courts.state.va.us/ocis-rest/api/public/getCourtsCodeDetails"]

	def parse(self, response):
		#gets to the relevant layer in the response json
		code_details = response.json()['context']['entity']['payload']
		for codes in code_details:
			try:
				codes['description']
			except KeyError:
				codes['description'] = "No description" 


			yield{
				'Court Category': codes['courtCategory'], #C for circuit, G for general
				'Code ID': codes['codeId'], 
				'Code Description': codes['description'], #code description, ie 'White' for code 'W'
				'Code Type': codes['codeType'] #variable code is describing
				}			
	

class court_codes(scrapy.Spider):
	#codes for each court based on fips of county/city
	name = "court_codes"

	start_urls = ["https://eapps.courts.state.va.us/ocis-rest/api/public/getLookupCodeDetails"]

	def parse(self, response):
		court_details = response.json()['context']['entity']['payload']['allCourts']
		for court in court_details:
			yield{
				'Court Name': court['courtName'], #actual name of court, like Accomack Circuit Court
				'Court ID': court['fipsCode4'] #court code used in website, like '001C'
				}		
