## General scrapy shell steps:

1. scrapy shell "https://eapps.courts.state.va.us/ocis/search"
2. accept = scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted")
3. fetch(accept)
4. searchRequestField = {
			"courtLevels":[],
 			"divisions":["Criminal/Traffic"],
 			"selectedCourts":[],
 			"searchString":["name here"],
 			"searchBy":"N"
 		}
5. search = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",method = "POST", data = searchRequestField)
6. fetch(search)
7. json_code = response.json()
8. case_results = json_code['context']['entity']['payload']['searchResults']
	- list of dicts, where each dict is the data to pass into the next request
9. get_details = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails", method = "POST", data = case_results[0])
10. json_code2 = response.json()
11. case_details = json_code2['context']['entity']['payload']
	- case_charge = case_details['caseCharge']['originalCharge']
		- charge_desc = case_charge['chargeDescriptionText']
		- charge_type = case_charge['caseTypeCode']
	- court = case_details['caseCourt']['fipsCode'] (as string)
	- sentencing = case_details['sentencingInformation']
	- probation? = case_details['disposition']['probationInfo']['probationType']
	- participant = case_details['caseParticipant'][0] - possible that there are more than 1
		- participant_name = participant['contactInformation']['personName']
		- participant_demo = participant['personalDetails']
			- {'race': 'W', 'gender': 'F', 'maskedBirthDate': '02/20'}
	- hearing = case_details['caseHearing'][0] - possible that there are more than 1
		- judge_id = hearing['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		- hearing_type = hearing['hearingJudge']['hearingResult']
12. not really part of shell, but to get codes for cases: scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCourtsCodeDetails")
13. and for courts: scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getLookupCodeDetails")

## Still to figure out
1. how to imitate request to load more
	- endingIndex: 30 in search field to get next 30 results
	- endingIndex does not exist when getting first 30
2. how to go back to the page of all cases from case details