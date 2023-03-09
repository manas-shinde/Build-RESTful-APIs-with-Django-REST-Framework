from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Belowed are Generie-based view


class ProductsList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return ProductSerializer


# Belowed are class-based views


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Deserialize the pass object
        serializer = ProductSerializer(data=request.data)

        # Validate the Object contains required fields
        serializer.is_valid(raise_exception=True)

        # To save the new Product to DB
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(APIView):
    def get(self, request, id):
        # Read the object from database using ID
        product = get_object_or_404(Product, pk=int(id))
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        # Read the object from database using ID
        product = get_object_or_404(Product, pk=int(id))
        # Deserialize the object
        serializer = ProductSerializer(data=request.data, instance=product)

        # validate the object
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        # Read the object from database using ID
        product = get_object_or_404(Product, pk=int(id))
        if product.orderitem_set.count() > 0:
            return Response({'can not delete this product becase order item are related to it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Generie based view


class CollectionList(ListCreateAPIView):
    # If you are not changing the serializer class based on user type then you can define this serializer class name with one line only
    serializer_class = CollectionSerializer
    # def get_serializer_class(self):
    #     return CollectionSerializer

    # same for queryset
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    # def get_queryset(self):
    #     return Collection.objects.annotate(
    #         products_count=Count('products')).all()

# Belowed are method based view


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
        serialier = CollectionSerializer(
            queryset, many=True)
        return Response(serialier.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serialier.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_details(request, pk):
    collections = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)

    if request.method == "GET":
        # Get serialize object
        serializer = CollectionSerializer(collections)

        # Return the serializer object data with status code 200
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        # De-serialize the object
        serializer = CollectionSerializer(
            data=request.data, instance=collections)

        # validate the object
        serializer.is_valid(raise_exception=True)

        serializer.save()

    elif request.method == "DELETE":
        if collections.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
