# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy, re
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
from w3lib.html import remove_tags

def findAllNumbers(value) :
    return re.findall(r'\d+', value)

def lastVal(value) :
    return value[-1]

def availabilityConverter(value) :
    return value == "In stock"

class AmazonItem(scrapy.Item) :
    # define the fields for your item here:
    availability = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip, availabilityConverter), output_processor = TakeFirst())
    itemName = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip), output_processor=Compose(lastVal, findAllNumbers, Join(""), int))
    rating = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip, Join("")), output_processor = Compose(TakeFirst(), float))
    noOfRatings = scrapy.Field(input_processor = MapCompose(remove_tags, str.strip, findAllNumbers, Join(""), int), output_processor = TakeFirst())
    itemLink = scrapy.Field(output_processor=TakeFirst())

class MyntraOrAjioItem(scrapy.Item) :
    # define the fields for your item here:
    availability = scrapy.Field(output_processor=TakeFirst())
    itemName = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    noOfRatings = scrapy.Field(output_processor=TakeFirst())
    itemLink = scrapy.Field(output_processor=TakeFirst())
