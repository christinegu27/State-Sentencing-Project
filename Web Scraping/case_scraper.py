import scrapy

# a general idea of what the spider will eventually do
# definitely do not crawl - everything is basically pseudocode and nothing actually works as intended

class case_scraper(scrapy.Spider):
	name = "my_case"

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	searchRequestField = {
			"courtLevels":["C"],
			"divisions":["Criminal/Traffic"],
			"selectedCourts":[],
			#"searchString":[name here],
			"searchBy":"N",
			#"endingIndex":0
		}

	#accepts terms and conditions
	def parse(self, response):
		return scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	#enters search terms
	def search(self, response):
		searchRequestField["endingIndex"] = 0
		#eventually, will have to do some type of looping with the search string to hit all possible names
		#for possible name in names
			searchRequestField["searchString"] = possible name
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = searchRequestField,
				callback = self.parse_cases)
	
	#sends request to access case details for all 30-ish results generated
	def parse_cases(self, response):
		case_results = response.json()['context']['entity']['payload']['searchResults']
		for case in case_results:
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails",
				method = "POST",
				data = case,
				callback = self.case_details)

		#repeats for all matching cases based on search criteria
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			#somehow add +30 to endingIndex from searchRequestField, then
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = searchRequestField,
				callback = self.parse_cases)

	def case_details(self, response):
		#actually get relevant details per case and send to csv