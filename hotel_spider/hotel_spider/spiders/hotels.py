# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import HotelSpiderItem
from ..items import HotelReviewItem
import time
import random

class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    allowed_domains = ['tripadvisor.in']
    start_urls = ['http://www.tripadvisor.in/Hotels-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html/']

    def parse_reviews(self,response):

        time.sleep(random.randrange(1,3))
        review_tabs = response.xpath('//div[@class="location-review-review-list-parts-SingleReview__mainCol--1hApa"]')

        for review_tab in review_tabs:
            review_loader = ItemLoader(item = HotelReviewItem(), selector = review_tab, response = response)
            
            review_loader.add_value('name',response.meta.get('name'))
            review_loader.add_xpath('review','div[@class="location-review-review-list-parts-ExpandableReview__containerStyles--1G0AE"]//q/span/text()')
            review_loader.add_xpath('bubbles','div[@class="location-review-review-list-parts-RatingLine__container--2bjtw"]/div[@class="location-review-review-list-parts-RatingLine__bubbles--GcJvM"]/span/@class')
            
            yield review_loader.load_item()

        data = {
            'name' : response.meta.get('name'),
        }
        
        next_review_url = response.xpath('//div[@class="location-review-pagination-card-PaginationCard__wrapper--3epz_"]/div[@class="ui_pagination is-centered"]/a[@class="ui_button nav next primary "]/@href').extract_first()
        absolute_next_url = response.urljoin(next_review_url)

        if absolute_next_url is not None :
            yield Request(absolute_next_url, callback=self.parse_reviews,meta = data)


    
    def parse_hotel(self,response):
        time.sleep(random.randrange(1,3))
        hotel_loader = ItemLoader(item = HotelSpiderItem(), response = response)
        
        header = response.xpath('//div[@id="taplc_hotel_review_atf_hotel_info_web_component_0"]')
        name = header.xpath('//h1[@id="HEADING"]/text()').extract_first()
        contact = header.xpath('//div[@class="hotels-hotel-review-atf-info-parts-ATFInfo__reverseActions--37dZ3"]')
        contact = contact.xpath('//div[@class="hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7"]')
        address_block = contact.xpath('//div[@class="hotels-hotel-review-atf-info-parts-BusinessListingEntry__entry--210S0 hotels-hotel-review-atf-info-parts-BusinessListingEntry__address--1Vy86"]')
        address = address_block.xpath('//span[@class="public-business-listing-ContactInfo__nonWebLink--2rxPP public-business-listing-ContactInfo__ui_link_container--37q8W public-business-listing-ContactInfo__level_4--3JgmI"]/span/text()').extract_first()
        phone = contact.xpath('//div[@class="hotels-hotel-review-atf-info-parts-BusinessListingEntry__entry--210S0 hotels-hotel-review-atf-info-parts-BusinessListingEntry__phone--1e9vv"]/div[@data-blcontact="PHONE "]/a/@href').extract_first()
        #website = contact.xpath('//div[@class="hotels-hotel-review-atf-info-parts-BusinessListingEntry__entry--210S0 hotels-hotel-review-atf-info-parts-BusinessListingEntry__phone--1e9vv"]/div[@data-blcontact="URL_HOTEL "]/a/@class').extract_first()

        review_div = response.xpath('//div[@class="ui_columns hotels-hotel-review-about-with-photos-layout-LayoutStrategy__columns--1uvt4"]')
        review_div = review_div.xpath('//div[@class="ui_column  "]')
        
        left_review_div = review_div[0]
        overall_rating = left_review_div.xpath('//div[@class="hotels-hotel-review-about-with-photos-Reviews__rating--2X_zZ hotels-hotel-review-about-with-photos-Reviews__cx_brand_refresh_phase2--3eimy"]/span/text()').extract_first()
        #left_review_div_rating_list = left_review_div.xpath('//div[@class="hotels-hotel-review-about-with-photos-Reviews__subratingRow--2u0CJ"]')
        
        
        right_review_div = review_div[1]
        amenities = right_review_div.xpath('div[@class="ssr-init-26f"]/@data-ssrev-handlers').extract_first()

        hotel_loader.add_value('name',name)
        hotel_loader.add_value('url',response.url)
        hotel_loader.add_value('address',address)
        hotel_loader.add_value('phone',phone)
        hotel_loader.add_value('overall_rating',overall_rating)
        hotel_loader.add_value('amenities',amenities)


        yield hotel_loader.load_item()

        review_tabs = response.xpath('//div[@class="location-review-review-list-parts-SingleReview__mainCol--1hApa"]')

        for review_tab in review_tabs:
            review_loader = ItemLoader(item = HotelReviewItem(), selector = review_tab, response = response)
            
            review_loader.add_value('name',name)
            review_loader.add_xpath('review','div[@class="location-review-review-list-parts-ExpandableReview__containerStyles--1G0AE"]//q/span/text()')
            review_loader.add_xpath('bubbles','div[@class="location-review-review-list-parts-RatingLine__container--2bjtw"]/div[@class="location-review-review-list-parts-RatingLine__bubbles--GcJvM"]/span/@class')
            
            yield review_loader.load_item()
        
        next_review_url = response.xpath('//div[@class="location-review-pagination-card-PaginationCard__wrapper--3epz_"]/div[@class="ui_pagination is-centered"]/a[@class="ui_button nav next primary "]/@href').extract_first()
        absolute_next_url = response.urljoin(next_review_url)

        data = {
            'name' : name,
        }

        yield Request(absolute_next_url, callback=self.parse_reviews, meta = data)
    
    def parse(self, response):
        time.sleep(random.randrange(1,3))
        main_div = response.xpath('//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]')
        div_list = main_div.xpath('//div[@class="meta_listing ui_columns large_thumbnail_mobile "]')
        
        for div in div_list:
            hotel_url = response.urljoin(div.xpath('@data-url').extract_first())
            yield Request(hotel_url, callback=self.parse_hotel)

        pagination = response.xpath('//div[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]')
        next_button = pagination.xpath('//div[@class="unified ui_pagination standard_pagination ui_section listFooter"]/a[@class="nav next ui_button primary  cx_brand_refresh_phase2"]/@href').extract_first()
        absolute_next_button = response.urljoin(next_button)

        yield Request(absolute_next_button, callback=self.parse)

    