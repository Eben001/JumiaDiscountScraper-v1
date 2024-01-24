# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join


class JumiaItem(scrapy.Item):
    name = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())
    seller_score = scrapy.Field(output_processor=Join())
    product_rating = scrapy.Field(output_processor=Join())
    original_price = scrapy.Field(output_processor=Join())
    discount_percentage = scrapy.Field(output_processor=Join())
    image_url = scrapy.Field(output_processor=Join())
    product_link = scrapy.Field(output_processor=Join())
    # expire_at = scrapy.Field()
