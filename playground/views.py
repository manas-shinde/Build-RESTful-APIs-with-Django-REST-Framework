from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__)


class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info("Calling httpbin")
            response = requests.get('https://httpbin.org/delay/3')
            data = response.json()
        except request.ConnectionError:
            logger.critical('httpbin is offline')
        logger.info('Response received from httpbin')
        return render(request, 'hello.html', {'name': data})

# @cache_page(5*60)
# def say_hello(request):
#     """ This is function based Cacheing View"""
#     response = requests.get('https://httpbin.org/delay/3')
#     data = response.json()
#     return render(request, 'hello.html', {'name': data})
