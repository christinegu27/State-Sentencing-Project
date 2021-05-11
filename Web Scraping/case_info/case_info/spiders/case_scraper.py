import scrapy
#from scrapy.shell import inspect_response


class case_scraper(scrapy.Spider):
	name = "cases"

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	letters = "abcdefghijklmnopqrstuvwxyz"

	#accepts terms and conditions
	def parse(self, response):
		yield scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	#enters search terms looping through alphabet
	def search(self, response):
		for letter1 in case_scraper.letters:
			for letter2 in case_scraper.letters:
				search = letter1+letter2
				yield scrapy.http.JsonRequest(
						url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
						method = "POST",
						data = {"courtLevels":["C"], 
								"divisions":["Criminal/Traffic"],
								"selectedCourts":[],
								"searchBy":"N", 
								"searchString": [search],
								"endingIndex" : 0},
						callback = self.check_results,
						cb_kwargs = dict(search_name = search))

	#checks if any matching results
	def check_results(self, response, search_name):
		#go back and try next letter combo if no matching results
		if response.json()['context']['entity']['payload']['noOfRecords'] == 0:
			#print(search_name, "...nothing here")
			return
		else: 
			yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = {"courtLevels":["C"], 
								"divisions":["Criminal/Traffic"],
								"selectedCourts":[],
								"searchBy":"N",
								"searchString":[search_name],
								"endingIndex":9930},
					callback = self.check_length,
					cb_kwargs = dict(search_name = search_name))

	#checks if current search string has too many results
	def check_length(self, response, search_name):
		#print(search_name)
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			for extra_letter in case_scraper.letters:
				base_name = search_name
				current_search = search_name+extra_letter
				yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = {"courtLevels":["C"], #circuit courts only
							"divisions":["Criminal/Traffic"],
							"selectedCourts":[],
							"searchBy":"N",
							"searchString":[current_search],
							"endingIndex":0},
					callback = self.check_results,
					cb_kwargs = dict(search_name = current_search))
		else:
			#print("parsing cases...", search_name)
			yield scrapy.http.JsonRequest(
					url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
					method = "POST",
					data = {"courtLevels":["C"], 
							"divisions":["Criminal/Traffic"],
							"selectedCourts":[],
							"searchBy":"N",
							"searchString":[search_name],
							"endingIndex":0},
					callback = self.parse_cases,
					cb_kwargs = dict(search_name = search_name))

	def parse_cases(self, response, search_name):
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
				data = {"courtLevels":["C"], #circuit courts only
						"divisions":["Criminal/Traffic"],
						"selectedCourts":[],
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
			probation_type = "No Probation"
			probation_years = probation_months = probation_days = 0

		try:
			judge = case_details['caseHearing'][0]['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		except KeyError:
			judge = "Unknown"

		yield{
			'Case Number': case_details['caseTrackingID'],
			'Name': case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'],
			'Court': case_details['caseCourt']['fipsCode'],
			'Last Hearing Date': case_details['caseHearing'][0]['courtActivityScheduleDay']['scheduleDate'],
			'Charge':case_details['caseCharge'][charge]['chargeDescriptionText'],
			'Charge Code': case_details['caseCharge'][charge].get('caseTypeCode'),
			'Charge Class': (case_details['caseCharge'][charge]).get('classCode'),
			'Charge Code Section': case_details['caseCharge'][charge]['codeSection'],
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