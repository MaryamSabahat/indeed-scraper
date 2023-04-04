import scrapy
from urllib.parse import urlencode
from scrapy_playwright.page import PageMethod
import w3lib
from db.connection import DBConnector
from datetime import datetime, timedelta


class CommentsSpider(scrapy.Spider):
    name = 'new_comments'
    allowed_domains = ['www.indeed.com']
    start_urls = [
        'https://www.indeed.com',
    ]

    headers = {
        'authority': 'www.indeed.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }

    def get_company_url(self, company):
        company = company.replace('.', '').replace(' ', '-')
        return f'{self.start_urls[0]}/cmp/{company}'

    def get_scrape_review_page(self, company, page=0):
        company_url = self.get_company_url(company)
        parameters = {'fcountry':'ALL', 'start': page * 20}
        return f'{company_url}/reviews?{urlencode(parameters)}'

    def start_requests(self):
        self.today_date = datetime.now().date() - timedelta(days=1)

        conn = DBConnector.Instance()
        companies = conn.get_all_compaies()
        # companies = self.conn.get_all_compaies()[0:50]
        # companies = ['Harris Teeter',]

        for company in companies:
            yield scrapy.Request(
                url=self.get_scrape_review_page(company), 
                headers=self.headers,
                meta={
                    'playwright': True,
                    'playwright_page_method': [
                        PageMethod('wait_for_selector', '.cmp-ReviewsList'),
                        PageMethod('wait_for_selector', '[data-testid=review-count]'),
                    ],
                    'company': company,
                    'page': 0,
                },
            )

    def parse(self, response, **kwargs):
        new_reviews = True
        new_messages = 0

        topic_list_filter = response.css('[data-testid=topic-filter-list]').css('.css-1vmx0e0::text').getall()

        reviews_list = response.css('.cmp-ReviewsList')
        reviews_list = reviews_list.css('[data-tn-entitytype="reviewId"]')

        review_count = response.css('[data-testid=review-count] > span::text').get()
        if review_count:
            review_count = review_count.split(' ')[2]
            review_count = review_count.replace(',', '')

        for review in reviews_list:
            try:
                rating = review.css('[itemprop="reviewRating"] > button::text').get()
                caption = w3lib.html.remove_tags(review.css('[data-testid="title"]').get())
                text = w3lib.html.remove_tags(review.css('[data-tn-component="reviewDescription"] > [itemprop="reviewBody"]').get())

                author_details = list(map(lambda s: s.strip(), w3lib.html.remove_tags(review.css('[itemprop="author"]').get()).split(' - ')))
                
                if date_format_change(author_details[2]) < self.today_date:
                    new_reviews = False
                    continue
            except:
                continue
            
            new_messages += 1

            yield {
                'company': response.meta['company'],
                'reviews_amount': review_count,
                'work_life_rate': topic_list_filter[0],
                'pay_benefits_rate': topic_list_filter[1],
                'security_adv_rate': topic_list_filter[2],
                'management_rate': topic_list_filter[3],
                'culture_rate': topic_list_filter[4],
                'reviewer_rate': rating,
                'caption': caption,
                'reviewer_position': author_details[0],
                'reviewer_location': author_details[1],
                'date_reviewed': date_format_change(author_details[2]),
                'text': text,
            }
        self.logger.info(f'By keyword [{response.meta["company"]}] taked [{new_messages}] new reviews')

        nex_page = response.css('[data-tn-element="next-page"]')
        if nex_page and new_reviews:
            meta_data = response.meta
            meta_data['page'] += 1 

            next_page_url = self.get_scrape_review_page(
                meta_data['company'],
                meta_data['page']
            )

            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                headers=self.headers,
                meta=meta_data,
            )

def date_format_change(date: str) -> datetime:
    date_format = {
        'June': 'Jun',
        'July': 'Jul',
        'August': 'Aug',
        'September': 'Sep',
        'October': 'Oct',
        'November': 'Nov',
        'December': 'Dec', 
        'January': 'Jan',
        'February': 'Feb',
        'March': 'Mar',
        'April': 'Apr',
        'May': 'May',
    }

    old_date_month = date.split(' ')[0]
    date_month = date_format[old_date_month]

    date = date.replace(old_date_month, date_month)
    
    return datetime.strptime(date, '%b %d, %Y').date()
