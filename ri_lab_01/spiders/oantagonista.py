# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class OantagonistaSpider(scrapy.Spider):
    name = 'oantagonista'
    start_urls = ['https://www.oantagonista.com/']
    # O construtor foi removido por estar ocasioando erro na chamada do json

    def parse(self, response): # funcao criada para pegar links da barra menu
        links = response.xpath('//ul//li//a[re:test(@href, "https://www.oantagonista.com/assuntos/")]/@href').getall()
        for link in links:
            yield scrapy.Request(
            response.urljoin(link),
            callback = self.parse_category
            )
    def parse_category(self,response): # pegando links das noticias

        news = response.css('a.article_link::attr(href)').getall()
        for new in news:
            yield scrapy.Request(
            response.urljoin(new),
            callback=self.parse_new
            )
    def parse_new(self, response): # entrando no link da noticia e salvando no arquivo csv
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

