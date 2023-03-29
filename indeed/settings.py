BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'

ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

CONCURRENT_REQUESTS = 1

LOG_LEVEL = 'DEBUG'

DOWNLOAD_DELAY = 3

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# PLAYWRIGHT_LAUNCH_OPTIONS = {
# 	"headless": False,
# 	"slow_mo": 50,
# 	# "proxy": { "server": "http://192.168.1.19:8889" },
# }
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 90000
PLAYWRIGHT_ABORT_REQUEST = lambda req: req.resource_type == "image"
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 1
