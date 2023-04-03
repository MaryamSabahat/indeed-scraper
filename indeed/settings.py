BOT_NAME = 'indeed'

SPIDER_MODULES = ['indeed.spiders']
NEWSPIDER_MODULE = 'indeed.spiders'

LOG_LEVEL = 'INFO'

ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

DOWNLOAD_DELAY = 0.5

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
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

