import scrapy
from scrapy.selector import Selector
import html2text

class AtlanticSpider(scrapy.Spider):
    name = "atlantic"
    
    website = 'https://www.theatlantic.com'
    addendum = '/latest/'
    start_urls=[website + addendum]

    def clean_text(self,text):

        text = text.replace("\n"," ")
        text = text.encode('ascii', 'ignore').decode('unicode_escape', 'ignore')
        return text

    
    def parse_article(self,response):
        hxs = Selector(response)
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        article = hxs.xpath("//section[contains(@id, 'article-section')]").extract()
        for section in article:
            text =  converter.handle(section)
            if text:
                text = self.clean_text(text)    
                yield{
                    'text' : text 
                }

    def parse(self,response):
        for datelink in response.xpath("//li[@class='article blog-article ']/a/@href").extract():
            if datelink is not None:
                url = self.website + datelink
                yield scrapy.Request(url, callback=self.parse_article)
        nextlink = response.xpath("//li[@class='next']/a/@href").extract_first()
        yield scrapy.Request(self.website + self.addendum + nextlink, callback=self.parse)
