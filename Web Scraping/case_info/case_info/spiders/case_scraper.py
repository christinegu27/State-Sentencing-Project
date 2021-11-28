import scrapy

class CaseSpider(scrapy.Spider):
	name = "cases_2"

	letters = "abcdefghijklmnopqrstuvwxyz"

	def __init__(self, court_code, *args, **kwargs):
		"""
		Initializes the spider as normal, but adds an instance variable
		keeping track of the court this spider will run
		"""
		super(CaseSpider, self).__init__(*args, **kwargs) #calls scrapy.Spider initializer
		self.court = court_code

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	def parse(self, response):
		"""
		Send request accepting TandC since website automaticlly redirects to the 
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
		for letter1 in CaseSpider.letters:
			for letter2 in CaseSpider.letters:
				search = letter1+letter2 
				#finds cases where the first or middle or last name starts with the search string given
				yield scrapy.http.JsonRequest(
						url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
						method = "POST",
						data = {"courtLevels":["C"], #searching circuit courts only
								"divisions":["Criminal/Traffic"], #limiting search to Criminal/Traffic cases only
								"selectedCourts":[self.court], #open to all available courts in Virginia
								"searchBy":"N", #searching by name (not case number or date)
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
		#add letter and try new combo if too many records records returned
		#continues looping until letters return less than 9960 results
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			for extra_letter in CaseSpider.letters:				
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
		"""
		Gathers case results and sends request to get more details. If there are more
		results, imitate a "load more" button by requesting the next set of cases
		search_name: current name string being searched
		"""
		#no results returned for the given search
		if response.json()['context']['entity']['payload']['noOfRecords'] == 0:
			return

		#each case has a matching json, basically stored as a list of dictionaries
		case_results = response.json()['context']['entity']['payload']['searchResults']

		for case in case_results: #first loops through all cases matching search
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails",
				method = "POST",
				data = case, #each entry is the json data in the request sent for more details 
				callback = self.case_details)

		#checks if there are more results to be loaded
		#"recursively" calls parsec_cases until all cases viewed
		if 'hasMoreRecords' in response.json()['context']['entity']['payload']:
			#the index of the first case in the next set results
			last_index = response.json()['context']['entity']['payload']['lastResponseIndex']
			yield scrapy.http.JsonRequest(
				url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
				method = "POST",
				data = {"courtLevels":["C"],
						"divisions":["Criminal/Traffic"],
						"selectedCourts":[self.court],
						"searchBy":"N",
						"searchString":[search_name],
						"endingIndex":last_index}, #sends new request loading next set of results
				callback = self.parse_cases,
				cb_kwargs = dict(search_name = search_name))

	def case_details(self, response):
		"""
		Gets relevant data from each case's detailed JSON file, then yields results
		as a dictionary 
		"""
		case_details = response.json()['context']['entity']['payload'] 

		#skip case if there is no sentence
		try:
			case_details['sentencingInformation']
		except KeyError:
			print("skipping case: ", case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'])
			return

		sentence=case_details['sentencingInformation']['sentence']

		#only gets final charge if charge was amended
		if "amendedCharge" in case_details['caseCharge']:
			charge = "amendedCharge"
		else:
			charge = "originalCharge"

		try: #checks if defendant was granted probation
			probation = case_details['disposition']['probationInfo']
			probation_type = probation['probationType']
			probation_years = probation['duration'].get('years')
			probation_months = probation['duration'].get('months')
			probation_days = probation['duration'].get('days')
		except KeyError: #otherwise set probation Y/M/D to 0
			probation_type = "NP"
			probation_years = probation_months = probation_days = 0

		try: #checks if case stored the presiding judge's ID (initials)
			judge = case_details['caseHearing'][0]['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		except KeyError:
			judge = "N/A"

		try: #checks if case stored the case's attorney 
			attorney = case_details['caseParticipant'][0]['attorneyDetails'][0]['attorneyName']['fullName']
		except KeyError:
			attorney = "N/A"


		yield{
			'Case Number': case_details['caseTrackingID'],
			'Name': case_details['caseParticipant'][0]['contactInformation']['personName']['fullName'], #defendant name
			'Court': case_details['caseCourt']['fipsCode'], #circuit court code
			'Last Hearing Date': case_details['caseHearing'][0]['courtActivityScheduleDay']['scheduleDate'],
			'Charge':case_details['caseCharge'][charge]['chargeDescriptionText'],
			'Charge Code': case_details['caseCharge'][charge].get('caseTypeCode'), #either Felony or Misdeamor
			'Charge Class': (case_details['caseCharge'][charge]).get('classCode'), #charge class (O, class 1, 2, etc.)
			#specific charge code as detailed in official "Code of Virginia"
			'Offense Date': case_details['caseCharge']['offenseDate'], 
			'Charge Code Section': case_details['caseCharge'][charge].get('codeSection'), 
			'Concluded By': case_details['disposition']['concludedByCode'], #guilty plea, trial with jury, etc.
			'Sentence Y': sentence.get('years'),
			'Sentence M': sentence.get('months'),
			'Sentence D': sentence.get('days'),
			'Probation Type': probation_type, # none granted, supervised, unsupervised, etc
			'Probation Y':probation_years,
			'Probation M':probation_months,
			'Probation D':probation_days,
			'Race': case_details['caseParticipant'][0]['personalDetails'].get('race'), 
			'Gender': case_details['caseParticipant'][0]['personalDetails'].get('gender'),
			'Birth date': case_details['caseParticipant'][0]['personalDetails'].get('maskedBirthDate'),
			'Judge': judge,
			'Attorney': attorney
			}
