# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class HotelSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    address = scrapy.Field(
        output_processor = TakeFirst()
    )
    phone = scrapy.Field(
        output_processor = TakeFirst()
    )
    overall_rating = scrapy.Field(
        output_processor = TakeFirst()
    )
    amenities = scrapy.Field(
        output_processor = TakeFirst()
    )

class HotelReviewItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    bubbles = scrapy.Field(
        output_processor = TakeFirst()
    )
    review = scrapy.Field(
        output_processor = TakeFirst()
    )