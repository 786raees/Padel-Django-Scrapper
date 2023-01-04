from django.contrib import admin
from .models import Country, State, City, Search
# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    '''Admin View for Country'''

    list_display = ('name',)
    search_fields = ('name',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    '''Admin View for State'''

    list_display = ('name','country',)
    list_filter = ('country',)
    search_fields = ('name','country')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    '''Admin View for City'''

    list_display = ('name','state','country',)
    list_filter = ('state','country',)
    search_fields = ('name','state','country',)

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    '''Admin View for Search'''

    list_display = ('id','name',)
    search_fields = ('id','name',)
    list_display_links = ('id','name',)
