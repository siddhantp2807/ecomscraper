import scrapy, json, random, time
from itemloaders import ItemLoader
from ecomscraper.items import MyntraOrAjioItem

class AJioSpider(scrapy.Spider) :

    name = "ajio"

    # start_urls = ["https://www.ajio.com/red-tape-round-toe-lace-up-sneakers/p/469419009_navy", "https://www.ajio.com/red-tape-low-top-lace-up-sneakers/p/466345463_white", "https://www.ajio.com/red-tape-mid-top-lace-up-sneakers/p/466330708_white"]

    def start_requests(self):
        for url in self.start_urls :
            self.random_delay()
            string = url.split('/p/')[-1]
            api_url = f"https://www.ajio.com/api/p/{string}"
            yield scrapy.Request(api_url, headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"}, callback=self.parse)
    
    def parse(self, response) :

        data = json.loads(response.text)
        loader = ItemLoader(item=MyntraOrAjioItem(), selector=data)

        availability = data['stock']['stockLevelStatus'] == "inStock"
        name = data["brandName"] + " " + data["name"]
        
        loader.add_value("availability", availability)
        loader.add_value("itemName", name)
        loader.add_value("price", data["price"]["value"])
        loader.add_value("rating", data["ratingsResponse"]["aggregateRating"]["averageRating"])
        loader.add_value("noOfRatings", int(data["ratingsResponse"]["aggregateRating"]["numUserRatings"]))
        loader.add_value("itemLink", response.url)

        # yield {
        #     "availability" : availability,
        #     "itemName" : name,
        #     "price" : price,
        #     "rating" : rating,
        #     "noOfRatings" : noOfRatings,
        #     "itemLink" : response.url
        # }

        yield loader.load_item()


    def random_delay(self) :
        
        delay = random.uniform(1, 5)
        time.sleep(delay)