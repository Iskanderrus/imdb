import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url="https://www.imdb.com/chart/top/", headers={"User_Agent": self.user_agent})

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=('//h3/a')),
            callback='parse_item',
            follow=True,
            process_request="set_user_agent"
        ),
    )

    def set_user_agent(self, request, response):
        request.headers["User-Agent"] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath('//h1/span/text()').get(),
            "year": response.xpath('(//section/div/div/ul/li[@role="presentation"])[1]/a/text()').get(),
            "age": response.xpath('(//section/div/div/ul/li[@role="presentation"])[2]/a/text()').get(),
            "duration": ' '.join(response.xpath(
                '((//div[@data-testid="title-techspecs-section"]/ul/li[1]/*)[2]/text())[1] | ((//div['
                '@data-testid="title-techspecs-section"]/ul/li[1]/*)[2]/text())[3] | ((//div['
                '@data-testid="title-techspecs-section"]/ul/li[1]/*)[2]/text())[5] | ((//div['
                '@data-testid="title-techspecs-section"]/ul/li[1]/*)[2]/text())[7]').getall()),
            "genre": response.xpath('//a/span[@class="ipc-chip__text"]/text()').get(),
            "rating": response.xpath(
                '//div[@class="sc-7b68ec71-0 fuKYWn sc-93323f1b-12 bmgiwi"]/div/div/a/span/div/div[2]/div/span['
                '1]/text()').get(),
            "user_reviews": response.xpath('//ul/li[1]/a/span/span[@class="score"]/text()').get(),
            "critic_reviews": response.xpath('//ul/li[2]/a/span/span[@class="score"]/text()').get(),
            "metascore": response.xpath('//span[@class="score-meta"]/text()').get(),
            "oscar_nominations": response.xpath('//div[@data-testid="awards"]/ul/li/a/text()').get(),
            "wins_and_nominations": response.xpath('//div[@data-testid="awards"]/ul/li/div/ul/li/span/text()').get(),
            "director": response.xpath('//section[@data-testid="title-cast"]/ul/li[1]//a/text()').get(),
            "country_of_origin": response.xpath('//div[@data-testid="title-details-section"]/ul/li[2]//a/text()').get(),
            "production_company": response.xpath(
                '//div[@data-testid="title-details-section"]/ul/li[7]//div//a/text()').get(),
            "movie_url": response.url,
        }
