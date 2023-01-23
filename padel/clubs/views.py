import contextlib
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import PadelClub, Record
from .filters import PadelClubFilter
from django.db.models import Subquery, OuterRef, Prefetch, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.conf import settings
from django.utils import timezone
from django.views.decorators.cache import cache_page
import json

def remove_dublicate(request):
    padels = PadelClub.objects.all()
    for padel in padels:
        new_padels = PadelClub.objects.filter(name=padel.name, city=padel.city).exclude(id=padel.id) # type: ignore
        for new_padel in new_padels:
            new_records = Record.objects.filter(padel_club=new_padel) # type: ignore
            new_records.update(padel_club__id=padel.id) # type: ignore
        new_padels.delete()
        padel.url = str(padel.url).split("?")[0]
        padel.save()

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

def add_dummy():
    ps = PadelClub.objects.all()[:10]
    Record.objects.all().update(created_at=datetime(2023,1,17))
    for i in ps:
        Record.objects.create(padel_club=i, no_of_courts=7, available_hours=30, booked_hours=26.5)

@cache_page(60 * 60)
def home(request):
    from_date_min = request.GET.get('from_date')
    from_date_max = request.GET.get('to_date')
    records_qs = Record.objects.select_related('padel_club')
    if from_date_min:
        from_date_min = datetime.strptime(from_date_min, '%Y-%m-%d')
        records_qs = records_qs.filter(created_at__gte=from_date_min)
    if from_date_max:
        from_date_max = datetime.strptime(from_date_max, '%Y-%m-%d')
        records_qs = records_qs.filter(created_at__lte=from_date_max)

    padel_clubs = PadelClub.objects.prefetch_related(Prefetch('record_set', queryset=records_qs))
    padel_clubs = padel_clubs.annotate(
        last_record_available_hours=Subquery(records_qs.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('available_hours')[:1]),
        last_record_booked_hours=Subquery(records_qs.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('booked_hours')[:1]),
        last_record_no_of_courts=Subquery(records_qs.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('no_of_courts')[:1]),
        last_record_utiliation_rate=Subquery(records_qs.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('utiliation_rate')[:1]),
        last_record_created_at=Subquery(records_qs.filter(padel_club=OuterRef('pk')).order_by('-created_at').values('created_at')[:1]),
    )
    if sort_by := request.GET.get("sort_by"):
        padel_clubs = padel_clubs.order_by(sort_by)
    

    filters = PadelClubFilter(request.GET, padel_clubs)
    padel_clubs = filters.qs.distinct()
    total_available_hours = float(sum(q.last_record_available_hours for q in padel_clubs if q.last_record_available_hours))
    total_booked_hours = float(sum(q.last_record_booked_hours for q in padel_clubs if q.last_record_booked_hours))

    year = timezone.now().year
    padel_clubs = padel_clubs.filter(last_record_created_at__year=year)

    months = [f"Jan-{year}", f"Feb-{year}", f"Mar-{year}", f"Apr-{year}", f"May-{year}", f"Jun-{year}", f"Jul-{year}", f"Aug-{year}", f"Sep-{year}", f"Oct-{year}", f"Nov-{year}", f"Dec-{year}"]

    data_set = padel_clubs.annotate(month=TruncMonth('last_record_created_at')).values('month').annotate(
    booked_hours_sum=Sum('last_record_booked_hours'),
    available_hours_sum=Sum('last_record_available_hours'),
    utilisation_rate_sum=(Sum('last_record_booked_hours') / Sum('last_record_available_hours')) * 100
    )

    chart_data = {
        month: {
        "booked_hours_sum" : 0.0,
        "available_hours_sum" : 0.0,
        "utiliation_rate_sum" : 0.0,
        }
        for month in months
    }


    for month_data in data_set:

        month = months[month_data['month'].month - 1]

        chart_data[month] = {
            "booked_hours_sum": float(month_data["booked_hours_sum"] or 0),
            "available_hours_sum": float(month_data["available_hours_sum"] or 0),
            "utiliation_rate_sum": float(month_data["utilisation_rate_sum"] or 0),
        }

    try:
        total_utiliation_rate = (total_booked_hours / total_available_hours) * 100
    except Exception:
        total_utiliation_rate = 0
    context = {
        'padels': PadelClub.objects.all(),
        'filters': filters,
        'padel_clubs': padel_clubs,
        "chart_data": json.dumps(chart_data),
        "total_available_hours": total_available_hours,
        "total_booked_hours": total_booked_hours,
        "total_utiliation_rate": '{:.2f}%'.format(total_utiliation_rate),
    
    }
    return render(request, "club/home.html", context)
