import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.case_scraper import CaseSpider

def court_crawl(crawler, court_code):
	return crawler.crawl(CaseSpider, court_code)

settings = get_project_settings()
settings['FEED_FORMAT'] = 'csv'
settings['FEED_URI'] = ''
crawler = CrawlerProcess(settings)
# "FEEDS": {"parallel_test.csv": {"format": "csv"},},

#167C Russell
#153C prince william
#085C hanover
#550C chesapeake
#810C virginia beach
#760C richmond city
courts  = ['167C', '153C', '085C', '550C', '810C', '760C']
for court in courts:
	settings.update({'FEED_URI': court + ".csv"})
	court_crawl(crawler, court_code = court)
crawler.start()


