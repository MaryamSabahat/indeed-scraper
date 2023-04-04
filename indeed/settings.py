BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'

LOG_LEVEL = 'INFO'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 1

CONCURRENT_REQUESTS = 1

ITEM_PIPELINES = {
    'indeed.pipelines.IndeedPipeline': 100,
}

DOWNLOAD_HANDLERS = {
    # Playwright
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    # Fake user agent
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}

FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

def should_abort_request(request):
    if request.resource_type == "image":
        return True
    if request.resource_type == "stylesheet":
        return True
    if request.resource_type == "script":
        return True
    if request.method.lower() == "post":
        return True
    
    return False


PLAYWRIGHT_ABORT_REQUEST = should_abort_request
