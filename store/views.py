from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
# Create your views here.


@api_view()
def product_list(request):
    return Response('OKAY !!!')


@api_view()
def product_detail(request, id):
    # return Response("ok")
    product = Product.objects.get(pk=int(id))
    serializer = ProductSerializer(product)
    return Response(serializer.data)
