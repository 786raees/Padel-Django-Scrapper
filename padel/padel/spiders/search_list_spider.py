import scrapy, re, json
from padel_app.wsgi import *
from location.models import Search

class SearchListSpiderSpider(scrapy.Spider):
    name = 'search_list_spider'
    start_urls = ['https://www.matchi.se']

    async def parse(self, response):
        search_data_css = '.form-group > script'
        script = response.css(search_data_css)
        script_data = script.xpath('.//text()').get()
        text = re.findall('source: (.+)',script_data)[0]
        json_data_list = json.loads(text)
        for data in json_data_list:
            search = await Search.objects.aget_or_create(name=data)
            yield {
                'data': data,
            }