import scrapy, re, random, time
from scrapy.loader import ItemLoader
from ecomscraper.items import MyntraOrAjioItem
import http.cookies, json


class MyntraSpider(scrapy.Spider) :

    name = "myntra"

    start_urls = ["https://www.myntra.com/casual-shoes/herenow/herenow-men-white--blue-comfort-insole-basics-sneakers/22605718/buy", "https://www.myntra.com/casual-shoes/asian/asian-men-white-sneakers/19706534/buy", "https://www.myntra.com/casual-shoes/asian/asian-men-grey-textured-sneakers/19925384/buy", "https://www.myntra.com/casual-shoes/asian/asian-men-grey-sneakers/20234358/buy"]

    def start_requests(self):
        
        first_url = self.start_urls[0]
        
        yield scrapy.Request(first_url, headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0" }, callback=self.get_data)


    def get_data(self, response) :

        cookie_bytes = response.request.headers.getlist("Cookie")[0]
        cookie_string = cookie_bytes.decode('utf-8')

        cookie_obj = http.cookies.SimpleCookie()
        cookie_obj.load(cookie_string)

        # Convert cookies to a dictionary
        cookies_dict = {cookie.key: cookie.value for cookie in cookie_obj.values()}
        cookies_dict["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"

        for url in self.start_urls :
            self.random_delay()
            num = re.findall(r'\d{8}', url)
            # https://www.myntra.com/gateway/v2/product/20234358
            api_url = f"https://www.myntra.com/gateway/v2/product/{num[0]}"
            yield scrapy.Request(api_url, headers=cookies_dict, callback=self.parse)
    
    def parse(self, response) :
        
        data = json.loads(response.text)["style"]
        loader = ItemLoader(item=MyntraOrAjioItem(), selector=data)

        prices = []
        for size in data["sizes"] :
            if size['sizeSellerData'] != [] and "discountedPrice" in size['sizeSellerData'][0].keys() :
                prices.append(size['sizeSellerData'][0]["discountedPrice"])

        availability = bool(prices)

        # yield {
        #     "availability" : availability,
        #     "itemName" : data["name"],
        #     "price" : min(prices),
        #     "rating" : data["ratings"]["averageRating"],
        #     "noOfRatings" : data["ratings"]["totalCount"],
        #     "itemLink" : response.url
        # }

        loader.add_value("availability", availability)
        loader.add_value("itemName", data["name"])
        loader.add_value("price", min(prices))
        loader.add_value("rating", data["ratings"]["averageRating"])
        loader.add_value("noOfRatings", data["ratings"]["totalCount"])
        loader.add_value("itemLink", response.url)

        yield loader.load_item()

    def random_delay(self) :
        delay = random.uniform(1, 5)
        time.sleep(delay)