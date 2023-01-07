import scrapy, json
from datetime import datetime
from typing import Dict
from padel_app.wsgi import *
from clubs.models import PadelClub, Record
from location.models import City

def format_address(address: Dict) -> str:
    return ''

def get_url(item: Dict) -> str:
    name = str(item.get('tenant_name')).lower().strip().replace(" ", "-")
    return f"https://playtomic.io/{name}/{item.get('tenant_id')}"

def get_today():
    return datetime.now().strftime('%Y-%m-%d')

class PlaytomicSpider(scrapy.Spider):
    name = 'playtomic'
    start_urls = ['https://playtomic.io/api/v1/tenants']

    def __init__(self, name=None, **kwargs):
        self.cities = [i[0].lower() for i in list(City.objects.all().values_list('name'))]
        super().__init__(name, **kwargs)

    def parse(self, response):
        json_data = json.loads(response.body)
        for data in json_data:
            
            if land:= data.get('address'):
                if land:= land.get('city'):
                    land = land.strip()
                    if land.lower() not in self.cities:
                        continue
                    tenant_id = data.get('tenant_id')
                    today = get_today()

                    url = f"https://playtomic.io/api/v1/availability?user_id=me&tenant_id={tenant_id}&sport_id=PADEL&local_start_min={today}T00%3A00%3A00&local_start_max={today}T23%3A59%3A59"
                    yield scrapy.Request(url=url, callback=self.parse_slot, cb_kwargs=data)


    async def parse_slot(self, response, **kwargs):
        json_data = json.loads(response.body)
        price_30_min, price_60_min, price_90_min, price_unit = None, None, None, None
        minutes = 0
        for resource in json_data:
            if slots:= resource.get('slots'):
                for slot in slots:
                    duration = slot.get('duration')
                    minutes += duration
                    price, price_unit = slot.get('price').split()[0], slot.get('price').split()[1]
                    if duration == 30:
                        price_30_min = price
                        continue

                    if duration == 60:
                        price_60_min = price
                        continue

                    if duration == 90:
                        price_90_min = price
                        continue
        slot_count = len(json_data)
        booked_hour = (minutes / 60) - (slot_count * 18)
        data = kwargs
        print("++++++++++++++++++++")
        print(data)
        print(booked_hour)
        print(slot_count)
        print(minutes)
        print(json_data)
        print("++++++++++++++++++++")
        padel, created = await PadelClub.objects.aget_or_create(
            name=data.get('tenant_name'),
            city=data.get('address', {'city':''}).get('city'),
            address = format_address(data.get('address')), # type: ignore
            url = get_url(data),
            price_30_min = price_30_min,
            price_60_min = price_60_min,
            price_90_min = price_90_min,
            price_unit = price_unit,
        )
        await Record.objects.acreate(
            padel_club = padel,
            booked_hours = booked_hour,
            available_hours = slot_count * 18,
            no_of_courts = slot_count,
        )