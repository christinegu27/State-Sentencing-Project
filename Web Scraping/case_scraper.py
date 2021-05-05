import scrapy
from scrapy.shell import inspect_response

# a general idea of what the spider will eventually do
# definitely do not crawl - everything is basically pseudocode and nothing actually works as intended

class case_scraper(scrapy.Spider):
	name = "cases"

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	searchRequestField = {
			"courtLevels":["C"], #circuit courts only
			"divisions":["Criminal/Traffic"],
			"selectedCourts":[],
			"searchBy":"N" #searching by name
		}

	letters = "abcdefghijklmnopqrstuvwxyz"

	#accepts terms and conditions
	def parse(self, response):
		yield scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	#enters search terms
	def search(self, response):
		case_scraper.searchRequestField["endingIndex"] = 0
		# for letter1 in case_scraper.letters:
		# 	for letter2 in case_scraper.letters:
		# 		search_name = letter1+letter2
		# 		case_scraper.searchRequestField["searchString"] = [search_name]
		# 		yield scrapy.http.JsonRequest(
		# 			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
		# 			method = "POST",
		# 			data = case_scraper.searchRequestField,
		# 			callback = self.check_results)
		case_scraper.searchRequestField["searchString"] = ["st"]
		yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = case_scraper.searchRequestField,
				callback = self.check_results)

	def check_results(self, response):
		#try next letter combo if no matching results
		if response.json()['context']['entity']['payload']['noOfRecords'] == 0:
			return

		#when more than 30 cases, check that max isn't too much
		else if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			case_scraper.searchRequestField["endingIndex"] = 9930
			yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = case_scraper.searchRequestField,
					callback = self.check_length)

		#ready to start getting further case details from first results
		case_scraper.searchRequestField['endingIndex'] == 0
		yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = case_scraper.searchRequestField,
					callback = self.parse_cases)

	#checks if current search string has too many results
	def check_length(self,response):
		#if true, then need to refine search
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			inspect_response(response, self)
			#gets the current "base" search - probably 2 characters
			base_search = case_scraper.searchRequestField["searchString"]
			for extra_letter in case_scraper.letters:
				current_search = base_search+extra_letter
				case_scraper.searchRequestField["searchString"] = [current_search]
				yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = case_scraper.searchRequestField,
					callback = self.check_results)
		#not too many cases, leave function
		return

	def parse_cases(self,response):
		
		inspect_response(response, self)
		case_results = response.json()['context']['entity']['payload']['searchResults']
		yield case
			# yield scrapy.http.JsonRequest(
			# 	url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails",
			# 	method = "POST",
			# 	data = case,
			# 	callback = self.case_details)

		#repeats for all matching cases based on search criteria
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
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