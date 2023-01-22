from django import forms
import django_filters

from .models import PadelClub


class PadelClubFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Name",lookup_expr="icontains")
    no_of_courts_gte = django_filters.NumberFilter(
        field_name="record__no_of_courts",
        lookup_expr='gte',
        label="No Of Courts from",
    )
    no_of_courts_lte = django_filters.NumberFilter(
        field_name="record__no_of_courts",
        lookup_expr='lte',
        label="No Of Courts To",
    )
    utiliation_rate_lte = django_filters.NumberFilter(
        field_name="record__utiliation_rate",
        lookup_expr='lte',
        label="Utilization Rate To",
    )
    utiliation_rate_gte = django_filters.NumberFilter(
        field_name="record__utiliation_rate",
        lookup_expr='gte',
        label="Utilization Rate From",
    )
    from_date = django_filters.DateFilter(
        field_name="record__created_at",
        label="From Data",
        lookup_expr="gte",
        # widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}), # type: ignore
    )
    to_date = django_filters.DateFilter(
        field_name="record__created_at",
        label="To Data",
        lookup_expr="lte",
        # widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}), # type: ignore
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.prefetch_related('record_set')

    class Meta:
        model = PadelClub
        fields = [
            "name",
            "city",
            "record__no_of_courts",
            "price_30_min",
            "price_60_min",
            "price_90_min",
        ]