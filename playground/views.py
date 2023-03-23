from django.shortcuts import render
import requests


def say_hello(request):
    requests.get('https://httpbin.org/delay/3')
    return render(request, 'hello.html', {'name': 'Mosh'})
