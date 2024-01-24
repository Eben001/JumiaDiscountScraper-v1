import scrapy
from scrapy.loader import ItemLoader

from jumia.items import JumiaItem
from urllib.parse import urljoin
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WomenJewelry(CrawlSpider):
    collection_name= "women_jewelry"
    name = "women_jewelry"
    allowed_domains = ["jumia.com.ng"]
    start_urls = ["https://www.jumia.com.ng/womens-jewelry/"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//a[@aria-label="Next Page"]'),
            callback='parse',
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//article[@class="prd _fb col c-prd"]/a[@class="core"]'),
            callback='parse_product'
        ),
    )

    def parse(self, response):
        pass 

    def parse_product(self, response):
        item = ItemLoader(item=JumiaItem(), response=response, selector=response)
        item.add_xpath("name", '//h1[@class="-fs20 -pts -pbxs"]/text()')
        item.add_xpath("price", '//span[contains(@class, "-b -ltr -tal -fs24 -prxs")]/text()')
        item.add_xpath("original_price", '//div[@class="-dif -i-ctr"]/span[1]/text()')
        item.add_xpath("discount_percentage", '//div[@class="-dif -i-ctr"]/span[2]/text()')
        item.add_xpath("seller_score", '//div[@class="-df -d-co -j-bet -prs"]/p/bdo/text()')
        item.add_xpath("product_rating", '//div[@class="stars _m _al"]/text()')
        item.add_xpath("product_link", './/link[@rel="canonical"]/@href')
        item.add_xpath("image_url", '//div[@class="-ptxs -pbs"]/div[@id="imgs"]/a/@href')
        
        yield item.load_item()