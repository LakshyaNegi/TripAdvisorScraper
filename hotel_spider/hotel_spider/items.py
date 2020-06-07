# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import re

def extract_phone(phone):
    temp = re.findall(r'\d+', phone) 
    res = list(map(int, temp))
    return res[0]

def extract_amenities(amenities):
    pass

def extract_bubbles(bubbles):
    bubbles = bubbles.split()
    bubbles = bubbles[-1]
    temp = re.findall(r'\d+', bubbles) 
    res = list(map(int, temp))
    res = res[0]/10
    return res

def extract_review(review):
    pass


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
        input_processor = MapCompose(extract_phone),
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
        input_processor = MapCompose(extract_bubbles),
        output_processor = TakeFirst()
    )
    review = scrapy.Field(
        output_processor = TakeFirst()
    )