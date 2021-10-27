import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import spiders.case_scraper
from spiders.case_scraper import CaseSpider

def court_crawl(process, court_code):
	#sets up a spider that will search through the provided court
	return process.crawl(CaseSpider, court_code)

settings = get_project_settings()#gets project settings
#sets up the output format
settings['FEED_FORMAT'] = 'csv'
settings['FEED_URI'] = ''
#creates a crawler process with given settings
process = CrawlerProcess(settings)

#load in list of circuit courts
url = "https://raw.githubusercontent.com/christinegu27/State-Sentencing-Project/main/Web%20Scraping/case_info/courts.csv"
courts = pd.read_csv(url)

for court in courts["Court ID"]:
	#create separate CSV file for each court
	settings.update({'FEED_URI': court + ".csv"})
	court_crawl(process, court_code = court)
process.start() #starts the spiders crawling


