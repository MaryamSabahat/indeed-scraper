import scrapy
from urllib.parse import urlencode
from pprint import pprint
import w3lib


class CommentsSpider(scrapy.Spider):
    name = 'comments'
    allowed_domains = ['www.indeed.com']
    start_urls = [
        'https://www.indeed.com/cmp/Schneider/reviews',
    ]

    def get_scrape_review_page(self, page=0):
        parameters = {"start": page * 20}
        return self.start_urls[0] + '?' + urlencode(parameters)

    def start_requests(self):
        for page in range(0, 10):
            yield scrapy.Request(
                url=self.get_scrape_review_page(page=page), 
                meta={
                    'playwright': True
                },
            )

        
    def parse(self, response, **kwargs):
        reviews_list = response.css('.cmp-ReviewsList')
        reviews_list = reviews_list.css('[data-tn-entitytype="reviewId"]')

        for review in reviews_list:
            rating = review.css('[itemprop="reviewRating"] > button::text').get()
            title = w3lib.html.remove_tags(review.css('[data-testid="title"]').get())
            description = w3lib.html.remove_tags(review.css('[data-tn-component="reviewDescription"] > [itemprop="reviewBody"]').get())

            author_details = list(map(lambda s: s.strip(), w3lib.html.remove_tags(review.css('[itemprop="author"]').get()).split(' - ')))
            
            yield {
                'rating': rating,
                'title': title,
                'company_name': author_details[0],
                'country': author_details[1],
                'post_date': author_details[2],
                'description': description,
            }
