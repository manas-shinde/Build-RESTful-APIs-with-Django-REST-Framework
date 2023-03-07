from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
# Create your views here.


@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(
        queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_list_or_404(Product, pk=int(id))
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view()
def collection_details(request, pk):
    # return Response("OK")
    collections = get_list_or_404(Collection, pk=int(pk))
    serializer = CollectionSerializer(collections)
    print(serializer)
    return Response(serializer.data)
