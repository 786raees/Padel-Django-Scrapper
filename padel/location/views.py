from django.shortcuts import render, HttpResponse
import subprocess
from django.conf import settings

def run_spider(request):
    subprocess.run(['python',settings.BASE_DIR/'manage.py','runscript','fill_search'])
    return HttpResponse('Ran Spider')
