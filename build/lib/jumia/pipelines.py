# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
import scrapy
from scrapy.exporters import PythonItemExporter
import re

class JumiaRemoveDuplicatePipeline:
    def __init__(self):
        self.product_name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        name = adapter.get('name')
        if name is None:
            spider.logger.warning(f"Item does not have a 'name' field: {item}")
            raise DropItem(f"Item does not have a 'name' field: {item}")

        if adapter['name'] in self.product_name_seen: 
            raise DropItem(f"Duplicate product detected: {item}")
        else: 
            self.product_name_seen.add(adapter["name"])
            return item


class JumiaRemoveNoDiscountPipeline:
    def process_item(self, item, spider): 
        adapter = ItemAdapter(item)
        if not adapter.get('discount_percentage'): 
            raise DropItem(f"Product with no discount percentage detected: {item}")
        else: 
            return item
        

class JumiaRemoveSymbolPipeline: 
    def process_item(self, item, spider): 
        adapter = ItemAdapter(item)
        
        raw_discount_percentage = adapter.get('discount_percentage')
        if raw_discount_percentage:
            adapter['discount_percentage'] = self.extract_float_value(raw_discount_percentage)

        seller_score = adapter.get('seller_score')
        if seller_score:
            adapter['seller_score'] = self.extract_float_value(seller_score)

        raw_price = adapter.get('price')
        if raw_price:
            adapter['price'] = self.convert_price(raw_price)

        raw_original_price = adapter.get('original_price')
        if raw_original_price:
            adapter['original_price'] = self.convert_price(raw_original_price)

        product_rating = adapter.get('product_rating')
        if product_rating:
            adapter['product_rating'] = self.extract_rating(product_rating)

        return item
    
    def convert_price(self, price):
        # Remove the '₦' symbol and commas, then handle ranges and convert to float
        price = price.replace('₦', '').replace(',', '').strip()
        # Check if the price is a range
        if ' - ' in price:
            start, end = map(float, price.split(' - '))
            # Calculate the average of the range
            return (start + end) / 2
        else:
            return float(price)
        
    


    def extract_float_value(self, value):
        # Extract a float value from a string (e.g., '94%' -> 94.0)
        return float(re.search(r'\d+\.*\d*', value).group())

    def extract_rating(self, product_rating):
        # Extract the first number from the product_rating field
        extracted_number = re.search(r'\d+\.*\d*', product_rating)
        return float(extracted_number.group()) if extracted_number else 0.0

    

# class JumiaGenerateAffLinkPipeline: 
#     def process_item(self, item, spider): 
#         adapter = ItemAdapter(item)
#         product_url = adapter.get('product_link')

#         affiliate_id = "a15aa631-4016-405a-9f1d-8a6d27042c25"
#         other_identifier = "306ad549-764c-349e-a497-cdd2d98c349a"

#         affiliate_link = f"https://kol.jumia.com/api/click/custom/{affiliate_id}/{other_identifier}?r={product_url}"
#         adapter['product_link'] = affiliate_link
#         return item

    

class MongoPipeline: 
    collection_name = ''

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongodb = mongo_db

    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider): 
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongodb]
        if hasattr(spider, 'collection_name'):
            self.collection_name = spider.collection_name
        
        # self.db[self.collection_name].create_index("expire_at", expireAfterSeconds=0)


    def close_spider(self, spider): 
        self.client.close()

    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # adapter['expire_at'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        self.db[self.collection_name].insert_one(adapter.asdict())
        return adapter.asdict()
    

    
   