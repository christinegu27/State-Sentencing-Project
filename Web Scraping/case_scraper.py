import scrapy

# a very untested probably incorrect start to a spider
# definitely do not crawl

class case_scraper(scrapy.Spider):
	name = "my_case"

	start_urls = ["https://eapps.courts.state.va.us/ocis/search"]

	#accepts terms and conditions
	def parse(self, response):
		return scrapy.Request(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/termsAndCondAccepted",
			callback = self.search)

	#enters search terms
	def search(self, response):
		searchRequestField = {
			"courtLevels":[],
			"divisions":["Criminal/Traffic"],
			"selectedCourts":[],
			"searchString":["victoria johnson smith"],
			"searchBy":"N"
		}
		return scrapy.http.JsonRequest(
			url = "https://eapps.courts.state.va.us/ocis-rest/api/public/search",
			method = "POST",
			data = searchRequestField,
			callback = self.parse_data)
	
	def parse_data(self, response):
		json_code = response.json()
		case_results = json_code['context']['entity']['payload']['searchResults']

	def case_details(self, reponse):
get case details request fields
{"qualifiedFips":"167C",
"courtLevel":"C",
"divisionType":"R",
"caseNumber":"0901049301",
"formattedCaseNumber":"CR09010493-01",
"name":"JOHNSON, VICTORIA SMITH",
"offenseDate":"06/08/2010",
"chargeAmended":false,
"codeSection":"19.2-306",
"chargeDesc":"VIOL. OF GOOD BEH. (RE-SENT.)",
"caseType":"F",
"hearingDate":"06/08/2010",
"courtName":"Russell Circuit Court"}