## General scrapy shell notes:

1. scrapy shell "https://eapps.courts.state.va.us/ocis/search"
2. accept = scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted")
3. fetch(accept)
4. searchRequestField = {
			"courtLevels":["C"],
 			"divisions":["Criminal/Traffic"],
 			"selectedCourts":[],
 			"searchString":["name here"],
 			"searchBy":"N",
 			"endingIndex": 0
 		}
5. search = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",method = "POST", data = searchRequestField)
6. fetch(search)
8. case_results = response.json()['context']['entity']['payload']['searchResults']
	- list of dicts, where each dict is the data to pass into the next request
9. get_details = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails", method = "POST", data = case_results[0])
10. fetch(get_details)
11. case_details = response.json()['context']['entity']['payload']  
	Now some possibly relevant things stored in the code:    
	- case_charge = case_details['caseCharge']['originalCharge']
		- **charge_desc** = case_charge['chargeDescriptionText']
		- **charge_type** = case_charge['caseTypeCode']
	- **court** = case_details['caseCourt']['fipsCode'] (as string)
	- **sentence** = case_details['sentencingInformation']
	- **probation?** = case_details['disposition']['probationInfo']['probationType']
	- participant = case_details['caseParticipant'][0] - possible that there are more than 1
		- participant_name = participant['contactInformation']['personName']
		- **participant_demo** = participant['personalDetails']
			- {'race': 'W', 'gender': 'F', 'maskedBirthDate': '02/20'}
	- hearing = case_details['caseHearing'][0] - possible that there are more than 1
		- **judge_id** = hearing['hearingJudge']['judicialOfficialBarMembership']['judicialOfficialBarIdentification']['identificationID']
		- hearing_type = hearing['hearingJudge']['hearingResult']
12. not really part of shell, but to get codes for case details: scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCourtsCodeDetails")
13. and for lookup info: scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getLookupCodeDetails")

## Presentation code
scrapy shell "https://eapps.courts.state.va.us/ocis/search"  
accept = scrapy.Request(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted")  
fetch(accept)  
searchRequestField = {
			"courtLevels":["C"],
 			"divisions":["Criminal/Traffic"],
 			"selectedCourts":[],
 			"searchString":["name here"],
 			"searchBy":"N",
 			"endingIndex": 0
 		}  
search = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search", method = "POST", data = searchRequestField)  
fetch(search)  
case_results = response.json()['context']['entity']['payload']['searchResults']  
while('hasMoreRecords' in response.json()['context']['entity']['payload']):  
	searchRequestField['endingIndex'] += 30  
    search = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search", method = "POST",data = searchRequestField)  
    fetch(search)  
    new_results=response.json()['context']['entity']['payload']['searchResults']  
    case_results.extend(new_results)  
get_details = scrapy.http.JsonRequest(url = "https://eapps.courts.state.va.us/ocis-rest/api/public/getCaseDetails", method = "POST", data = case_results[0])
fetch(get_details)
response.json()
