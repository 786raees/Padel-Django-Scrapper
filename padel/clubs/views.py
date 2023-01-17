import contextlib
from django.shortcuts import render
from .models import PadelClub, Record
from .filters import PadelClubFilter
from django.db.models import Sum, Count, Max, Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.conf import settings
from django.utils import timezone

import json

def add_city():
    from location.models import Country, City
    country = "USA"
    country, created = Country.objects.get_or_create(name=country)
    city_names = ["Aberdeen", "Abilene", "Akron", "Albany", "Albuquerque", "Alexandria", "Allentown", "Amarillo", "Anaheim", "Anchorage", "Ann Arbor", "Antioch", "Apple Valley", "Appleton", "Arlington", "Arvada", "Asheville", "Athens", "Atlanta", "Atlantic City", "Augusta", "Aurora", "Austin", "Bakersfield", "Baltimore", "Barnstable", "Baton Rouge", "Beaumont", "Bel Air", "Bellevue", "Berkeley", "Bethlehem", "Billings", "Birmingham", "Bloomington", "Boise", "Boise City", "Bonita Springs", "Boston", "Boulder", "Bradenton", "Bremerton", "Bridgeport", "Brighton", "Brownsville", "Bryan", "Buffalo", "Burbank", "Burlington", "Cambridge", "Canton", "Cape Coral", "Carrollton", "Cary", "Cathedral City", "Cedar Rapids", "Champaign", "Chandler", "Charleston", "Charlotte", "Chattanooga", "Chesapeake", "Chicago", "Chula Vista", "Cincinnati", "Clarke County", "Clarksville", "Clearwater", "Cleveland", "College Station", "Colorado Springs", "Columbia", "Columbus", "Concord", "Coral Springs", "Corona", "Corpus Christi", "Costa Mesa", "Dallas", "Daly City", "Danbury", "Davenport", "Davidson County", "Dayton", "Daytona Beach", "Deltona", "Denton", "Denver", "Des Moines", "Detroit", "Downey", "Duluth", "Durham", "El Monte", "El Paso", "Elizabeth", "Elk Grove", "Elkhart", "Erie", "Escondido", "Eugene", "Evansville", "Fairfield", "Fargo", "Fayetteville", "Fitchburg", "Flint", "Fontana", "Fort Collins", "Fort Lauderdale", "Fort Smith", "Fort Walton Beach", "Fort Wayne", "Fort Worth", "Frederick", "Fremont", "Fresno", "Fullerton", "Gainesville", "Garden Grove", "Garland", "Gastonia", "Gilbert", "Glendale", "Grand Prairie", "Grand Rapids", "Grayslake", "Green Bay", "GreenBay", "Greensboro", "Greenville", "Gulfport-Biloxi", "Hagerstown", "Hampton", "Harlingen", "Harrisburg", "Hartford", "Havre de Grace", "Hayward", "Hemet", "Henderson", "Hesperia", "Hialeah", "Hickory", "High Point", "Hollywood", "Honolulu", "Houma", "Houston", "Howell", "Huntington", "Huntington Beach", "Huntsville", "Independence", "Indianapolis", "Inglewood", "Irvine", "Irving", "Jackson", "Jacksonville", "Jefferson", "Jersey City", "Johnson City", "Joliet", "Kailua", "Kalamazoo", "Kaneohe", "Kansas City", "Kennewick", "Kenosha", "Killeen", "Kissimmee", "Knoxville", "Lacey", "Lafayette", "Lake Charles", "Lakeland", "Lakewood", "Lancaster", "Lansing", "Laredo", "Las Cruces", "Las Vegas", "Layton", "Leominster", "Lewisville", "Lexington", "Lincoln", "Little Rock", "Long Beach", "Lorain", "Los Angeles", "Louisville", "Lowell", "Lubbock", "Macon", "Madison", "Manchester", "Marina", "Marysville", "McAllen", "McHenry", "Medford", "Melbourne", "Memphis", "Merced", "Mesa", "Mesquite", "Miami", "Milwaukee", "Minneapolis", "Miramar", "Mission Viejo", "Mobile", "Modesto", "Monroe", "Monterey", "Montgomery", "Moreno Valley", "Murfreesboro", "Murrieta", "Muskegon", "Myrtle Beach", "Naperville", "Naples", "Nashua", "Nashville", "New Bedford", "New Haven", "New London", "New Orleans", "New York", "New York City", "Newark", "Newburgh", "Newport News", "Norfolk", "Normal", "Norman", "North Charleston", "North Las Vegas", "North Port", "Norwalk", "Norwich", "Oakland", "Ocala", "Oceanside", "Odessa", "Ogden", "Oklahoma City", "Olathe", "Olympia", "Omaha", "Ontario", "Orange", "Orem", "Orlando", "Overland Park", "Oxnard", "Palm Bay", "Palm Springs", "Palmdale", "Panama City", "Pasadena", "Paterson", "Pembroke Pines", "Pensacola", "Peoria", "Philadelphia", "Phoenix", "Pittsburgh", "Plano", "Pomona", "Pompano Beach", "Port Arthur", "Port Orange", "Port Saint Lucie", "Port St. Lucie", "Portland", "Portsmouth", "Poughkeepsie", "Providence", "Provo", "Pueblo", "Punta Gorda", "Racine", "Raleigh", "Rancho Cucamonga", "Reading", "Redding", "Reno", "Richland", "Richmond", "Richmond County", "Riverside", "Roanoke", "Rochester", "Rockford", "Roseville", "Round Lake Beach", "Sacramento", "Saginaw", "Saint Louis", "Saint Paul", "Saint Petersburg", "Salem", "Salinas", "Salt Lake City", "San Antonio", "San Bernardino", "San Buenaventura", "San Diego", "San Francisco", "San Jose", "Santa Ana", "Santa Barbara", "Santa Clara", "Santa Clarita", "Santa Cruz", "Santa Maria", "Santa Rosa", "Sarasota", "Savannah", "Scottsdale", "Scranton", "Seaside", "Seattle", "Sebastian", "Shreveport", "Simi Valley", "Sioux City", "Sioux Falls", "South Bend", "South Lyon", "Spartanburg", "Spokane", "Springdale", "Springfield", "St. Louis", "St. Paul", "St. Petersburg", "Stamford", "Sterling Heights", "Stockton", "Sunnyvale", "Syracuse", "Tacoma", "Tallahassee", "Tampa", "Temecula", "Tempe", "Thornton", "Thousand Oaks", "Toledo", "Topeka", "Torrance", "Trenton", "Tucson", "Tulsa", "Tuscaloosa", "Tyler", "Utica", "Vallejo", "Vancouver", "Vero Beach", "Victorville", "Virginia Beach", "Visalia", "Waco", "Warren", "Washington", "Waterbury", "Waterloo", "West Covina", "West Valley City", "Westminster", "Wichita", "Wilmington", "Winston", "Winter Haven", "Worcester", "Yakima", "Yonkers", "York", "Youngstown"]
    for city in city_names:
        City.objects.get_or_create(country=country, name=city)

    country = "UK"
    with open(settings.BASE_DIR / 'UK.json', "r") as f:
        country, created = Country.objects.get_or_create(name=country)
        cities = json.load(f)
        for city in cities:
            with contextlib.suppress(Exception):
                City.objects.get_or_create(country=country, name=city.get('city'))


def home(request):
    # add_city()
    current_year = timezone.now().year
    last_record = Record.objects.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('no_of_courts', 'booked_hours', 'available_hours','utiliation_rate')[:1]
    padels = PadelClub.objects.annotate(
        last_record_no_of_courts=Subquery(last_record.values('no_of_courts')),
        last_record_booked_hours=Subquery(last_record.values('booked_hours')),
        last_record_available_hours=Subquery(last_record.values('available_hours')),
        last_record_utiliation_rate=Subquery(last_record.values('utiliation_rate')),
    )

    if sort_by := request.GET.get("sort_by"):
        padels = PadelClub.objects.all().order_by(sort_by)
    else:
        padels = padels.prefetch_related('record_set')

    filters = PadelClubFilter(request.GET, queryset=padels)
    qs = filters.qs.distinct()
    records_id_list = qs.annotate(
                    last_record_id=Max("record__id")
                    ).values_list("last_record_id", flat=True)
    from_date_min = request.GET.get('from_date_min')
    from_date_max = request.GET.get('from_date_max')
    records = Record.objects.filter(id__in=records_id_list, created_at__year=current_year)
    if from_date_min:
        records = records.filter(created_at__gte=from_date_min)
        qs = qs.filter(record_created_at__gte=from_date_min)
    if from_date_max:
        records = records.filter(created_at__lte=from_date_max)
        qs = qs.filter(record_created_at__lte=from_date_max)


    records_by_month = records.annotate(month=TruncMonth('created_at')).values('month').annotate(booked_hours_sum=Sum('booked_hours')).annotate(available_hours_sum=Sum('available_hours')).annotate(utiliation_rate_sum=Sum('utiliation_rate')).order_by('month')
    year = current_year
    months = [f"Jan-{year}", f"Feb-{year}", f"Mar-{year}", f"Apr-{year}", f"May-{year}", f"Jun-{year}", f"Jul-{year}", f"Aug-{year}", f"Sep-{year}", f"Oct-{year}", f"Nov-{year}", f"Dec-{year}"]

    chart_data = {
        month: {
        "booked_hours_sum" : 0.0,
        "utiliation_rate_sum" : 0.0,
        "available_hours_sum" : 0.0,
        }
        for month in months
    }
    for month_data in records_by_month:
        month = month_data['month']
        month = month.strftime('%h-%Y')

        chart_data[month]["booked_hours_sum"] = float(month_data['booked_hours_sum'])
        chart_data[month]["utiliation_rate_sum"] = float(month_data['utiliation_rate_sum'])
        chart_data[month]["available_hours_sum"] = float(month_data['available_hours_sum'])


    total_booked_hours = 0
    total_available_hours = 0
    for pad in qs:
        # if pad.record_set.last(): # type: ignore
        total_booked_hours += pad.last_record_booked_hours or 0  # type: ignore
        total_available_hours += pad.last_record_available_hours or 0  # type: ignore
    try:
        util_rate = (total_booked_hours / total_available_hours) * 100
    except Exception:
        util_rate = 0
    context = {
        "filters": filters,
        "padels": padels,
        "total_booked_hours": total_booked_hours,
        "total_available_hours": total_available_hours,
        "chart_data": json.dumps(chart_data),
        "total_utiliation_rate": '{:.2f}%'.format(util_rate),
    }
    return render(request, "club/home.html", context)
