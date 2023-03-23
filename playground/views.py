from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import requests


@cache_page(5*60)
def say_hello(request):
    """ This is function based Cacheing View"""
    response = requests.get('https://httpbin.org/delay/3')
    data = response.json()
    return render(request, 'hello.html', {'name': data})
