import scrapy, random, time
from ecomscraper.items import AmazonItem
from scrapy.loader import ItemLoader

class AmazonSpider(scrapy.Spider) :

    name = 'amazon'

    start_urls = ['https://www.amazon.in/dp/B0C9LNHR8Y/', 'https://www.amazon.in/dp/B0C1S6V34M/', 'https://www.amazon.in/dp/B0C6DYLM82/', 'https://www.amazon.in/dp/B0BVBC5RQG/']

    def start_requests(self) :
        for url in self.start_urls :
            self.random_delay()
            yield scrapy.Request(url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"}, callback=self.parse)
    
    def parse(self, response) :

        loader = ItemLoader(item = AmazonItem(), selector=response)

        loader.add_css("availability", "div#availability span.a-color-success")
        loader.add_css("itemName", "span#productTitle")
        loader.add_css("price", ".priceToPay span")
        loader.add_css("rating", "span.a-size-base.a-color-base")
        loader.add_css("noOfRatings", "span#acrCustomerReviewText")
        loader.add_value("itemLink", response.url)

        # item["availability"] = response.css('div#availability span.a-color-success::text').get().strip()
        # item["itemName"] = response.css('span#productTitle::text').get().strip()
        # item["price"] = int("".join(re.findall(r'\d+', response.css('.priceToPay span::text').getall()[-1])))
        # item["rating"] = float("".join(response.css('span.a-size-base.a-color-base::text').get().strip()))
        # item["noOfRatings"] = int("".join(re.findall(r'\d+', response.css('span#acrCustomerReviewText::text').get())))

        yield loader.load_item()


    def random_delay(self) :
        
        delay = random.uniform(1, 5)
        time.sleep(delay)