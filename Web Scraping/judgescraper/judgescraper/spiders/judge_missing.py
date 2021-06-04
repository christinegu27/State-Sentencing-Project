#for courts that got skipped with the main judges spider
import scrapy

class JudgeSpider(scrapy.Spider):
	name = "judges_missing"
	#gets the earliest page available for each missing court
	start_urls = [ 
	"https://web.archive.org/web/20020616142724/http://www.courts.state.va.us/courts/circuit/alleghany/home.html",
	"https://web.archive.org/web/20020707211840/http://www.courts.state.va.us/courts/circuit/arlington/home.html",
	"https://web.archive.org/web/20010917020228/http://www.courts.state.va.us/courts/circuit/bristol/home.html",
	"https://web.archive.org/web/20020511093747/http://www.courts.state.va.us/courts/circuit/chesapeake/home.html",
	"https://web.archive.org/web/20000901032429/http://www.courts.state.va.us/courts/circuit/clifton_forge/home.html",
	"https://web.archive.org/web/20000901031741/http://www.courts.state.va.us/courts/circuit/danville/home.html",
	"https://web.archive.org/web/20010426142744/http://www.courts.state.va.us/courts/circuit/fauquier/home.html",
	"https://web.archive.org/web/20010830014222/http://www.courts.state.va.us/courts/circuit/floyd/home.html",
	"https://web.archive.org/web/20010426142916/http://www.courts.state.va.us/courts/circuit/frederick/home.html",
	"https://web.archive.org/web/20010903013942/http://www.courts.state.va.us/courts/circuit/hanover/home.html",
	"https://web.archive.org/web/20000901024427/http://www.courts.state.va.us/courts/circuit/henrico/home.html",
	"https://web.archive.org/web/20010426135404/http://www.courts.state.va.us/courts/circuit/Prince_William/home.html",
	"https://web.archive.org/web/20000824060229/http://www.courts.state.va.us/courts/circuit/richmond/home.html",
	"https://web.archive.org/web/20010526124829/http://www.courts.state.va.us/courts/circuit/Roanoke_City/home.html",
	"https://web.archive.org/web/20011119121748/http://www.courts.state.va.us/courts/circuit/Roanoke_County/home.html",
	"https://web.archive.org/web/20010426141746/http://www.courts.state.va.us/courts/circuit/Rockingham/home.html",
	"https://web.archive.org/web/20000901032157/http://www.courts.state.va.us/courts/circuit/Scott/home.html",
	"https://web.archive.org/web/20010426100907/http://www.courts.state.va.us/courts/circuit/Shenandoah/home.html",
	"https://web.archive.org/web/20010526121400/http://www.courts.state.va.us/courts/circuit/Stafford/home.html",
	"https://web.archive.org/web/20011116092039/http://www.courts.state.va.us/courts/circuit/Virginia_Beach/home.html",
	"https://web.archive.org/web/20010117041900/http://www.courts.state.va.us:80/courts/circuit/Winchester/home.html",
	"https://web.archive.org/web/20010113154100/http://www.courts.state.va.us/courts/circuit/Wise/home.html",
	"https://web.archive.org/web/20040918095514/http://www.courts.state.va.us/courts/circuit/York_County_Poquoson/home.html"]

	def parse(self, response):
		year = response.css("td.c")[2].attrib["title"][-4:] #gets year of wayback maching capture
		#gets court that judges belong to
		try:
			#for psot-2005 website format
			court = response.xpath('//h1').extract()[0].split("\n")[1].strip()
		except IndexError: #old website format
			court = response.xpath('//*[@valign = "middle"]//font[@size = "6"]//text()').extract_first()
			court = court[1:-1]

		#will skip for loop if page is in old format
		for judge in response.css("li.judges").css("::text").extract():
			yield {
				"Judge": judge,
				"Year":year,
				"Court": court
			}

		#will skip for loop is page is in new format
		for row in response.xpath('//*[@width = "170"]//td[@width="164"]//text()').extract():
			if "Hon" in row: #only gets rows with judge names
				judge = row[3:-2]
				yield {
					"Judge":judge,
					"Year":year,
					"Court": court
					}

		next_page = response.css("td.f a")[2].attrib["href"] 

		if next_page: #follow next page link
			yield scrapy.Request(next_page, callback = self.parse)
	