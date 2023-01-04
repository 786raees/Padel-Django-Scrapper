from django.shortcuts import render
from .models import PadelClub, Record
from .filters import PadelClubFilter
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json


def home(request):
    current_year = timezone.now().year

    if sort_by := request.GET.get("sort_by"):
        padels = PadelClub.objects.all().order_by(sort_by)
    else:
        padels = PadelClub.objects.all()

    filters = PadelClubFilter(request.GET, queryset=padels)
    if filters.qs:
        records_id_list = [padel.record_set.last().id for padel in filters.qs if padel.record_set.last()]
    else:
        records_id_list = [padel.record_set.last().id for padel in padels if padel.record_set.last()] # type: ignore
    from_date_min = request.GET.get('from_date_min')
    from_date_max = request.GET.get('from_date_max')
    records = Record.objects.filter(id__in=records_id_list, created_at__year=current_year)
    if from_date_min:
        records = records.filter(created_at__gt=from_date_min)
    if from_date_max:
        records = records.filter(created_at__lt=from_date_max)


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
    for pad in filters.qs:
        if pad.record_set.last(): # type: ignore
            total_booked_hours += pad.record_set.last().booked_hours or 0  # type: ignore
            total_available_hours += pad.record_set.last().available_hours or 0  # type: ignore
    util_rate = (total_booked_hours / total_available_hours) * 100
    context = {
        "filters": filters,
        "padels": padels,
        "total_booked_hours": total_booked_hours,
        "total_available_hours": total_available_hours,
        "chart_data": json.dumps(chart_data),
        "total_utiliation_rate": '{:.2f}%'.format(util_rate),
    }
    return render(request, "club/home.html", context)
