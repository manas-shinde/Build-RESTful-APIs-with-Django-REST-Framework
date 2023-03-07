from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        # Deserialize the pass object
        serializer = ProductSerializer(data=request.data)
        # Validate the Object contains required fields
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('ok')


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
    return Response(serializer.data)
