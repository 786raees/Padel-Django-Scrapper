from django.contrib import admin
from .models import PadelClub, Record

class RecordInline(admin.TabularInline):
    model = Record
    fields =  (
        "booked_hours",
        "available_hours",
        "no_of_courts",
        "utiliation_rate",
    )
    extra = 0


@admin.register(PadelClub)
class PadelClubAdmin(admin.ModelAdmin):
    """Admin View for PadelClub"""

    list_display = (
        "name",
        "city",
        # "booked_hours",
        # "available_hours",
        # "utiliation_rate",
        "price_30_min",
        "price_60_min",
        "price_90_min",
        "price_unit",
    )

    inlines = [RecordInline]
    search_fields = ("name",)
    date_hierarchy = "record__created_at"
    ordering = ("-created_at",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Admin View for Record"""

    list_display = (
        "padel_club",
        "no_of_courts",
        "booked_hours",
        "available_hours",
        "utiliation_rate",
        "created_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
# @admin.register(Slot)
# class SlotAdmin(admin.ModelAdmin):
#     """Admin View for Slot"""

#     list_display = (
#         "club",
#         "title",
#         "date",
#         "start_time",
#         "end_time",
#         "price",
#         "currency",
#         "is_booked",
#         "is_not_available",
#     )
#     search_fields = ("title",)
#     date_hierarchy = "created_at"
#     ordering = ("-created_at",)
