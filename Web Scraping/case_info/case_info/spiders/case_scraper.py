import scrapy
from scrapy.crawler import CrawlerProcess

class CaseSpider(scrapy.Spider):
	name = "cases_2"

	letters = "abcdefghijklmnopqrstuvwxyz"

	def __init__(self, court_code, *args, **kwargs):
		super(CaseSpider, self).__init__(*args, **kwargs)
		self.court = court_code

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	def parse(self, response):
		"""
		Send request "acceptint" TandC since website automaticlly redirects to the 
		TandC page when starting spider
		"""
		yield scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	def search(self, response):
		"""
		Sends request to generate cases matching a specified search.
		Starts sith all possible 2 letter permutations.
		"""
		for letter1 in case_scraper.letters:
			for letter2 in case_scraper.letters:
				search = letter1+letter2 
				#finds cases where the first or middle or last name starts with the search string given
				yield scrapy.http.JsonRequest(
						url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
						method = "POST",
						data = {"courtLevels":["C"], #searching circuit courts only
								"divisions":["Criminal/Traffic"], #limiting search to Criminal/Traffic cases only
								"selectedCourts":[self.court], #open to all available courts in Virginia
								"searchBy":"N", #searching by name (not case number of date)
								"searchString": [search],
								"endingIndex" : 9930}, #jumps straight to the end 
						callback = self.check_results,
						cb_kwargs = dict(search_name = search)) #saves current search string for later use
		
	def check_results(self, response, search_name):
		"""
		Checks if current search string returns too many results and repeats search after adding
		another letter. If not too many results, calls function to start parsing cases.
		search_name: current search name string passed from request
		"""
		#add letter and try new combo if too many records returned
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			for extra_letter in case_scraper.letters:				
				base_name = search_name
				current_search = search_name+extra_letter
				yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = {"courtLevels":["C"], 
							"divisions":["Criminal/Traffic"],
							"selectedCourts":[self.court],
							"searchBy":"N",
							"searchString":[current_search],
							"endingIndex":9930}, 
					callback = self.check_results,
					cb_kwargs = dict(search_name = current_search))
		else: 
			yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = {"courtLevels":["C"], 
								"divisions":["Criminal/Traffic"],
								"selectedCourts":[self.court],
								"searchBy":"N",
								"searchString":[search_name],
								"endingIndex":0},
					callback = self.parse_cases,
					cb_kwargs = dict(search_name = search_name))

	def parse_cases(self, response, search_name):
		#no results for search
		if response.json()['context']['entity']['payload']['noOfRecords'] == 0:
			return

		case_results = response.json()['context']['entity']['payload']['searchResults']
		for case in case_results:
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails",
				method = "POST",
				data = case,
				callback = self.case_details)

		#repeats for all matching cases based on search criteria
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			last_index = response.json()['context']['entity']['payload']['lastResponseIndex']
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = {"courtLevels":["C"],
						"divisions":["Criminal/Traffic"],
						"selectedCourts":[self.court],
						"searchBy":"N",
						"searchString":[search_name],
						"endingIndex":last_index},
				callback = self.parse_cases,
				cb_kwargs = dict(search_name = search_name))

	def case_details(self, response):
		case_details = response.json()['context']['entity']['payload'] 

		#skip case if no sentence given
		try:
			case_details['sentencingInformation']
		except KeyError:
			print("skipping case: ", case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'])
			return

		sentence=case_details['sentencingInformation']['sentence']

		#only gets final charge 
		if "amendedCharge" in case_details['caseCharge']:
			charge = "amendedCharge"
		else:
			charge = "originalCharge"

		try:
			probation = case_details['disposition']['probationInfo']
			probation_type = probation['probationType']
			probation_years = probation['duration'].get('years')
			probation_months = probation['duration'].get('months')
			probation_days = probation['duration'].get('days')
		except KeyError:
			probation_type = "NP"
			probation_years = probation_months = probation_days = 0

		try:
			judge = case_details['caseHearing'][0]['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		except KeyError:
			judge = "N/A"

		yield{
			'Case Number': case_details['caseTrackingID'],
			'Name': case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'],
			'Court': case_details['caseCourt']['fipsCode'],
			'Last Hearing Date': case_details['caseHearing'][0]['courtActivityScheduleDay']['scheduleDate'],
			'Charge':case_details['caseCharge'][charge]['chargeDescriptionText'],
			'Charge Code': case_details['caseCharge'][charge].get('caseTypeCode'),
			'Charge Class': (case_details['caseCharge'][charge]).get('classCode'),
			'Charge Code Section': case_details['caseCharge'][charge].get('codeSection'),
			'Concluded By': case_details['disposition']['concludedByCode'],
			'Sentence Y': sentence.get('years'),
			'Sentence M': sentence.get('months'),
			'Sentence D': sentence.get('days'),
			'Probation Type': probation_type,
			'Probation Y':probation_years,
			'Probation M':probation_months,
			'Probation D':probation_days,
			'Race': case_details['caseParticipant'][0]['personalDetails'].get('race'), 
			'Gender': case_details['caseParticipant'][0]['personalDetails'].get('gender'),
			'Judge': judge
			}