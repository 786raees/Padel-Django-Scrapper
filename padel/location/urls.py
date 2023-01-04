from .views import run_spider
from django.urls import path

urlpatterns = [
    path('spider/run/', run_spider, name="run_spider"),
]
