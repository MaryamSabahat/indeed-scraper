import scrapy
from urllib.parse import urlencode
from scrapy_playwright.page import PageMethod
import w3lib


class CommentsSpider(scrapy.Spider):
    name = 'all_comments'
    allowed_domains = ['www.indeed.com']
    start_urls = [
        'https://www.indeed.com',
    ]

    def get_company_url(self, company):
        company = company.replace(' ', '-')
        return f'{self.start_urls[0]}/cmp/{company}'

    def get_scrape_review_page(self, company, page=0):
        company_url = self.get_company_url(company)
        parameters = {'fcountry':'ALL', 'start': page * 20}
        return f'{company_url}/reviews?{urlencode(parameters)}'

    def start_requests(self):
        companies = ['Schneider', 'Schnaider']
        for company in companies:
            yield scrapy.Request(
                url=self.get_scrape_review_page(company), 
                meta={
                    'playwright': True,
                    'playwright_page_method': [
                        PageMethod('wait_for_selector', '.cmp-ReviewsList')
                    ],
                    'company': company,
                    'page': 0,
                },
            )

        
    def parse(self, response, **kwargs):
        reviews_list = response.css('.cmp-ReviewsList')
        reviews_list = reviews_list.css('[data-tn-entitytype="reviewId"]')

        self.logger.info(f'Page [{response.meta["page"] + 1}] for keyword [{response.meta["company"]}] has {len(reviews_list)} elements')
        for review in reviews_list:
            rating = review.css('[itemprop="reviewRating"] > button::text').get()
            title = w3lib.html.remove_tags(review.css('[data-testid="title"]').get())
            description = w3lib.html.remove_tags(review.css('[data-tn-component="reviewDescription"] > [itemprop="reviewBody"]').get())

            author_details = list(map(lambda s: s.strip(), w3lib.html.remove_tags(review.css('[itemprop="author"]').get()).split(' - ')))
            
            yield {
                'keyword': response.meta['company'],
                'rating': rating,
                'title': title,
                'company_name': author_details[0],
                'country': author_details[1],
                'post_date': author_details[2],
                'description': description,
            }
        
        nex_page = response.css('[data-tn-element="next-page"]')
        if nex_page:
            meta_data = response.meta
            meta_data['page'] += 1 

            next_page_url = self.get_scrape_review_page(
                meta_data['company'],
                meta_data['page']
            )

            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                meta=meta_data,
            )

