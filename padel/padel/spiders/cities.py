import scrapy
from padel_app.wsgi import *
from location.models import Country, City, State
import asyncio

class CitiesSpider(scrapy.Spider):
    name = 'cities'
    start_urls = ['https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068']

    async def parse(self, response):
        country = "USA"
        country, created = await Country.objects.aget_or_create(name=country)
        states = response.xpath("//section[contains(@id,'ref3266')]")
        for state in states:

            state_name = state.xpath(".//h2/a/text()").get()
            state_name, created = await State.objects.aget_or_create(country=country, name=state_name)
            cities = state.xpath('.//ul/li/div/a/text()').getall()
            for city in cities:
                city, created = await City.objects.aget_or_create(country=country, state=state_name, name=city)
                # yield {
                #     'Country': country.name,
                #     'State': state_name.name,
                #     'City': city.name,
                # }
