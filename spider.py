import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
setup()


class Crawler(scrapy.Spider):
    name = "SEFAAuthors"

    start_urls = [
        "https://pureportal.coventry.ac.uk/en/organisations/school-of-economics-finance-and-accounting/publications/"
    ]

    custom_settings = {
        "FEEDS": {
            "authors.csv": {
                "format": "csv",
                "overwrite": True
            }
        }
    }

    def parse(self, response):
        page = response

        for item in page.css('li.list-result-item'):
            title = item.css('h3.title span::text').get()
            authors = item.css('a.person span::text').getall()
            date = item.css('span.date::text').get()
            pub_link = item.css('h3.title a.link::attr(href)').extract()
            author_profile = item.css('a.person::attr(href)').getall()
            yield {
                "Title": title,
                "Authors": authors,
                'Date': date,
                'Pureportal': author_profile,
                'Pub Link': pub_link
            }

        next_page = response.css('a.nextLink::attr(href)').extract()

        if next_page is not None or len(next_page) > 0:
            next_page = response.urljoin(next_page[0])
            yield scrapy.Request(next_page, callback=self.parse)


@wait_for(100)
def run_code():
    my_spider = CrawlerRunner()
    code = my_spider.crawl(Crawler)
    return code


run_code()
