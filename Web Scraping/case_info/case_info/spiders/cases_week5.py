import scrapy

# a general idea of what the spider will eventually do
# definitely do not crawl - everything is basically pseudocode and nothing actually works as intended

class case_scraper(scrapy.Spider):
	name = "cases_presentation"

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	searchRequestField = {
			"courtLevels":["C"],
			"divisions":["Criminal/Traffic"],
			"selectedCourts":[],
			#"searchString":[name here],
			"searchBy":"N"
			#"endingIndex":0
		}

	#accepts terms and conditions
	def parse(self, response):
		yield scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	#enters search terms
	def search(self, response):
		names = ["victoria miller", "victoria johnson smith"]
		#eventually, will have to do some type of looping with the search string to hit all possible names
		for name in names:
			case_scraper.searchRequestField["searchString"] = [name]
			case_scraper.searchRequestField["endingIndex"] = 0
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = case_scraper.searchRequestField,
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
			case_scraper.searchRequestField['endingIndex'] += 30
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = case_scraper.searchRequestField,
				callback = self.parse_cases)

	def case_details(self, response):
		case_details = response.json()['context']['entity']['payload'] 

		#skip case if no sentence given
		try:
			case_details['sentencingInformation']
		except KeyError:
			return

		sentence=case_details['sentencingInformation']['sentence']

		try:
			judge = case_details['caseHearing'][0]['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		except KeyError:
			judge = "Unknown"

		yield{
			'Case Number': case_details['caseTrackingID'],
			'Name': case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'],
			'Court': case_details['caseCourt']['fipsCode'],
			'Last Hearing Date': case_details['caseHearing'][0]['courtActivityScheduleDay']['scheduleDate'],
			'Charge':case_details['caseCharge']['originalCharge']['chargeDescriptionText'],
			'Sentence Y': sentence.get('years'),
			'Sentence M': sentence.get('months'),
			'Sentence D': sentence.get('days'),
			'Race': case_details['caseParticipant'][0]['personalDetails']['race'],
			'Gender': case_details['caseParticipant'][0]['personalDetails']['gender'],
			'Judge': judge
			}