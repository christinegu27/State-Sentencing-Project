# Scrapy settings for case_info project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'case_info'

SPIDER_MODULES = ['case_info.spiders']
NEWSPIDER_MODULE = 'case_info.spiders'

# DOWNLOADER_MIDDLEWARES = {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610}
# ZYTE_SMARTPROXY_ENABLED = True
# ZYTE_SMARTPROXY_APIKEY = '5c80ab581940400eb78802469bcb78a1'

#CLOSESPIDER_PAGECOUNT = 100

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'case_info (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

ITEM_PIPELINES = {
    # 'case_info.pipelines.CasesPipeline': 800,
    'case_info.pipelines.CasesPipeline': 300
    # 'case_info.pipelines.DaPipeline': 200,

}

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

