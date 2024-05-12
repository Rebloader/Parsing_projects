import scrapy
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from ..items import Seminar6Item


class SpiderImagesSpider(CrawlSpider):
    name = "spider_images"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/images/sports/football"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='Prxeh']")), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='UYsLB VfiJa ec_09 Niw9H _UNLg']/button[@type='button']")))
    )

    def parse(self, response):
        loader = ItemLoader(item=Seminar6Item(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath("author_image", "//div[@class='TeuLI']/a/text()")

        loader.add_xpath('Published', '//time/text()')

        categories = response.xpath('//div[@class="zDHt2 N9mmz"]/a/text()').getall()
        loader.add_value('categories', categories)

        description = response.xpath("//div[@class='WxXog']/img/@alt").get()
        loader.add_value('description', description)

        image_url = response.xpath("//div[@class='WxXog']/img/@src").get()
        loader.add_value('image_urls', image_url)

        yield loader.load_item()
