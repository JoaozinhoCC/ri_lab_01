# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    start_urls = ['https://www.oantagonista.com/']

    def parse(self, response):
        links = response.xpath('//ul//li//a[re:test(@href, "https://www.oantagonista.com/assuntos/")]/@href').getall()
        for link in links:
            yield scrapy.Request(
            response.urljoin(link),
            callback = self.parse_category
            )
    def parse_category(self,response):

        news = response.css('a.article_link::attr(href)').getall()
        for new in news:
            yield scrapy.Request(
            response.urljoin(new),
            callback=self.parse_new
            )
    def parse_new(self, response):
        title = response.css('article h1::text').get()
        date = response.css('article time::text').get()
        text = response.css('article p::text').get()
        author = response.css('article.comment-body footer div b.fn::text').get()
        category = response.css('span a::text').get()
        yield{
        'title' : title,
        'date' : date,
        'text' : text,
        'auhor' : author,
        'category' : category,
        'url' : response.url
        }
