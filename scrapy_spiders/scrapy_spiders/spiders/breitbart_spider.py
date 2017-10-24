import scrapy
from scrapy.selector import Selector
import html2text

URL_FORMAT = "http://breitbart.com/{}/"
CATEGORIES = ['big-government', 'big-journalism', 'big-hollywood', 'national-security',
        'tech', 'sports', 'london', 'jersualem', 'texas', 'california']
start = []
for category in CATEGORIES:
    start.append(URL_FORMAT.format(category))

class BreitbartSpider(scrapy.Spider):

    name = "breitbart"
    start_urls= start

    def clean_text(self,text):

        text = text.replace("\n"," ")
        text = text.encode('ascii', 'ignore').decode('unicode_escape', 'ignore')
        return text

    
    def parse_article(self,response):
        hxs = Selector(response)
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        article = hxs.xpath("//div[@class='entry-content']").extract_first()
        text =  converter.handle(article)
        if text:
            text = self.clean_text(text)    
            yield{
                    'text' : text 
                }

    def parse(self,response):
        for hyperlink in response.xpath("//div[@class='article-list']/article/a/@href").extract():
            if hyperlink is not None:
                url = hyperlink
                yield scrapy.Request(url, callback=self.parse_article)
        nextlink = response.xpath("//div[@class='pagination']/div[@class='alignleft']/a/@href").extract_first()
        yield scrapy.Request(nextlink, callback=self.parse)
