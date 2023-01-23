import contextlib
import scrapy, re, requests
from scrapy.http import FormRequest
from padel_app.wsgi import *
from clubs.models import PadelClub, Record
from location.models import City

def get_time_def(hour):
    width = hour.css("::attr(title)").get()
    times = int(
        width.split("<br>")[-1]
        .strip()
        .split(" - ")[0]
        .replace("00:", "24:")
        .replace(":", "")
    )
    timee = int(
        width.split("<br>")[-1]
        .strip()
        .split(" - ")[1]
        .replace("00:", "24:")
        .replace(":", "")
    )
    time = timee - times
    _book = 0
    if time in [170, 130]:
        _book = 1.5
    elif time == 100:
        _book = 1
    elif time in [30, 70]:
        _book = 0.5
    else:
        print(timee, times)
    return _book



class MatchiSpider(scrapy.Spider):
    name = "matchi"
    # start_urls = ['https://www.matchi.se/book/findFacilities']
    def __init__(self, name=None, **kwargs):
        self.cities = list(City.objects.all().values_list('name'))
        
        super().__init__(name, **kwargs)
    def start_requests(self):
        login_url = "https://www.matchi.se/j_spring_security_check"
        yield FormRequest(
            login_url,
            formdata={
                "j_username": "xarovo6769@diratu.com",
                "j_password": "SadHappya1!",
                "_spring_security_remember_me": "on",
            },
            callback=self.start_scraping,
        )

    def start_scraping(self, response):
        res = requests.get('https://www.matchi.se/book/findFacilities')
        items = int(re.findall('<span class="results-label">(.+) results</span>',res.text)[0])
        pages, remaining_items = divmod(items, 10)
        if remaining_items > 0:
            pages += 1

        for page in range(pages):
            yield scrapy.Request(
                url=f"https://www.matchi.se/book/findFacilities?offset={page}0", callback=self.parse
            )

    def parse(self, response):
        # pagination: str = response.xpath(
        #     "//span[@class='results-label']/text()"
        # ).get()
        # pagination = int(pagination.split()[0])
        # page, reminder = divmod(pagination, 10)
        containers = response.css(
            "div.panel.panel-default.no-border.no-box-shadow.bottom-border"
        )

        for container in containers:
            url = container.css(
                "h3.media-heading.h4 a::attr(href)"
            ).get()
            url = url.split("?")[0]
            slot_urls = container.css(
                "div.slots-container a::attr(href)"
            ).getall()
            land = container.xpath(".//div/p[@class='text-muted text-sm']/text()").get()
            land = land.strip()
            if (land,) not in self.cities:
                continue

            
            for slot_url in slot_urls:
                with contextlib.suppress(Exception):
                    if _id := re.findall("facilityId=(.+)&start=", slot_url)[0]:
                        absolute_url = f"https://www.matchi.se{url}"
                        yield scrapy.Request(
                            absolute_url,
                            callback=self.get_padel_data,
                            cb_kwargs={"id": _id, "land": land},
                        )
                        break

    def get_padel_data(self, response, **kwargs):
        title: str = response.css("h2.h4.vertical-margin5::text").get()
        land: str = kwargs.get("land")  # type: ignore
        address: str = response.css(".panel-body dl dd.info::attr(title)").get()
        _id = kwargs.get("id")
        
        cb_k = {
            "id": _id,
            "title": title.strip(),
            "land": land.strip(),
            "address": address,
            "url": response.url,
        }

        yield scrapy.Request(
            url=f"https://www.matchi.se/book/schedule?facilityId={_id}",
            callback=self.parse_slot,
            cb_kwargs=cb_k,
        )

    async def parse_slot(self, response, **kwargs):
        booked = 0
        available = []
        available_slot_id = []
        booked_hours = response.css('tr[height="50"] td.red')
        for hour in booked_hours:
            difference = get_time_def(hour)
            booked += difference
        available_hours = response.css('tr[height="50"] td.free')
        for hour in available_hours:
            difference = get_time_def(hour)
            if difference not in available:
                temp_data = {
                    "slotid": hour.css("::attr(slotid)").get(),
                    "hour": difference,
                }
                available_slot_id.append(temp_data)
                available.append(difference)
        data = {
            'available_slot_id': available_slot_id,
            **kwargs,
            "Booked Hours": booked,
            "Available Hours": len(response.css('tr[height="50"]')) * 18,
            "No Of Courts": len(response.css('tr[height="50"]')),
        }
        padel, created = await PadelClub.objects.aget_or_create(
           name = data.get('title'),
           city = data.get('land'),
           address = data.get('address'),
           url = data.get('url'),
        )
        await Record.objects.acreate(
            padel_club = padel,
            booked_hours = data.get('Booked Hours'),
            available_hours = data.get('Available Hours'),
            no_of_courts = data.get('No Of Courts'),
        )
        data['padel'] = padel
        for slot in available_slot_id:
            slotID = slot.get("slotid")
            facilityId = data.get("id")
            url = response.css(f'a[href*="{slotID}"]::attr(href)').get()
            start = re.findall("&start=(.+)&end=", url)[0]
            end = re.findall("&end=(.+)&sportIds", url)[0]
            data['slotID'] = slotID
            url = "https://www.matchi.se/bookingPayment/confirm"
            yield FormRequest(
                url,
                formdata={
                    "slotIds": slotID,
                    "facilityId": facilityId,
                    "start": start,
                    "end": end,
                },
                callback=self.get_slot_data,
                cb_kwargs=data,
            )

    async def get_slot_data(self, response, **kwargs):
        min_30 = ''
        min_60 = ''
        min_90 = ''
        unit = ''
        data = kwargs
        try:
            unit = response.css('span[id*="bookingPrice_"]::text').get().split()[1]
            price = response.css('span[id*="bookingPrice_"]::text').get().split()[0]
        except Exception:
            price = None
        slots = data['available_slot_id']
        padel = PadelClub.objects.filter(id=data.get('padel').id) # type: ignore
        for slot in slots:
            if slot['slotid']==data['slotID']:
                if slot['hour']==0.5:
                    min_30 = price
                    await padel.aupdate(
                    price_30_min = min_30,
                    )
                elif slot['hour']==1:
                    min_60 = price
                    await padel.aupdate(
                    price_60_min = min_60,
                    )
                elif slot['hour']==1.5:
                    min_90 = price
                    await padel.aupdate(
                    price_90_min = min_90,
                    price_unit = unit,
                    )
        await padel.aupdate(
        price_unit = unit,
        )

