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

# #load in list of circuit courts
# url = "https://github.com/christinegu27/State-Sentencing-Project/blob/main/CSV%20Processing/courts.csv"
# courts = pd.read_csv(url,error_bad_lines=False)

# courts = ['001C','003C','005C','007C','009C','011C','013C','015C','017C','019C','021C','023C','520C','025C','027C','029C','530C','031C','033C','035C','036C',
# 	  '037C','540C','550C','041C','043C','560C','570C','045C','047C','049C','590C','051C','053C','057C','061C','063C','065C','067C','069C','630C','071C',
# 	  '073C','075C','077C','079C','081C','083C','650C','085C','087C','089C','091C','670C','093C','097C','099C','101C','103C','105C','107C','109C', '111C',
# 	  '680C','113C','690C','115C','117C','119C','121C','125C','127C','700C','710C','131C','133C','135C','137C','139C','141C','730C','143C','740C','145C',
# 	  '147C','149C','153C','155C','750C', '157C', '760C', '159C', '770C', '161C', '163C', '165C', '167C', '775C', '169C', '171C', '173C', '175C', '177C', 
# 	  '179C', '790C', '800C', '181C', '183C', '185C', '810C', '18C', '191C', '820C', '193C', '830C', '840C', '195C', '197C', '199C']

courts = ['091C']

for court in courts:
	#create separate CSV file for each court
	settings.update({'FEED_URI': court + ".csv"})
	court_crawl(process, court_code = court)
process.start() #starts the spiders crawling


