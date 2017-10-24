import scrapy
from scrapy.selector import Selector
import html2text

website = "https://www.newyorker.com"

class NewYorkerSpider(scrapy.Spider):

    name = "newyorker"
    start_urls= [website + "/latest"] 

    def clean_text(self,text):

        text = text.replace("\n"," ")
        text = text.encode('ascii', 'ignore').decode('unicode_escape', 'ignore')
        return text

    
    def parse_article(self,response):
        hxs = Selector(response)
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        article = hxs.xpath("//div[@id='articleBody']").extract_first()
        text =  converter.handle(article)
        if text:
            print("woohoo!")
            text = self.clean_text(text)    
            yield{
                    'text' : text 
                }

    def parse_page(self,response):
        for hyperlink in response.xpath("//h4[@class='River__hed___re6RP']/a/@href").extract():
            if hyperlink is not None:
                url = website + hyperlink
                yield scrapy.Request(url, callback=self.parse_article)

    def parse(self, response):
        last = response.xpath("//li[@class = 'Pagination__listItem___1hFiK']/a/@href").extract()[-1]
        page_prefix = "/latest/page/{}"
        last_number = int(last[-4:]) #last four digits of the page link - number of pages
        for i in range(1,last_number):
            url = website + page_prefix.format(str(i))
            yield scrapy.Request(url, callback=self.parse_page)

