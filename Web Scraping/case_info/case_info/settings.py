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

#CLOSESPIDER_PAGECOUNT = 100

DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'case_info (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 12

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'case_info.middlewares.CaseInfoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 500,
}

# USER_AGENTS = [
# 	('Mozilla/5.0 (Windows NT 10.0; Win64; x64)	'
# 	'AppleWebKit/537.36 (KHTML, like Gecko)	'
# 	'Chrome/74.0.3729.169	'
# 	'Safari/537.36'),
# 	('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) '
# 	'Gecko/20100101	'
# 	'Firefox/88.0'),
# 	('Mozilla/5.0 (Windows NT 10.0; WOW64) '
# 	'AppleWebKit/537.36 (KHTML, like Gecko)	'
# 	'Chrome/72.0.3626.121	'
# 	'Safari/537.36'),
# 	('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
# 	'AppleWebKit/537.36 (KHTML, like Gecko)	'
# 	'Chrome/90.0.4430.93	'
# 	'Safari/537.36'),
# 	('Mozilla/5.0 (Windows NT 10.0; Win64; x64)	'
# 	'AppleWebKit/537.36 (KHTML, like Gecko)	'
# 	'Chrome/90.0.4430.93	'
# 	'Safari/537.36'),
# 	('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6)	'
# 	'AppleWebKit/605.1.15 (KHTML, like Gecko)	'
# 	'Version/14.0.3	'
# 	'Safari/605.1.15')
# 	]

# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'case_info.pipelines.CaseInfoPipeline': 300,
#}

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

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
