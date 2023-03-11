from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter

# ModelViewset


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # To display reviews for specific product only
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    # To access the product id from the url
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    # def get_queryset(self):
    #     """Customize filter for product list based on collection id

    #     Returns:
    #         _type_: _description_
    #     """
    #     queryset = Product.objects.all()

    #     collection_id = self.request.query_params.get('collection_id')

    #     if collection_id:
    #         queryset = queryset.filter(collection_id=collection_id)

    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):

        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'can not delete this product becase order item are related to it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
        # This destory() is same logic that we've writen in delete() then only difference is the if condition that we have before deleteing product . so that why we just move condition above and just call destory() to do deleteion.


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()

    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs["pk"])
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


# Belowed are Generie-based view


class ProductsList(ListCreateAPIView):
    """So we dont need to write the get ,put and delete method implementation becase we were not doing any thing extra rather than reading , editing and deleting object without doing extra condition to check. 
    we can write queryset in get_queryset() or we can directly assign to variable called queryset as I implemented for CollectionList (Generie View).

    Args:
        ListCreateAPIView (_type_): To create a APIView with minimum implementation.
    """

    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        return ProductSerializer


# Belowed are class-based views


class ProductList(APIView):
    """In class based Views we dont need to write multiple if-else condition to check the request method , we can write the implementation to particular class method (get(),put() , etc).

    Args:
        APIView (_type_): _description_
    """

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


class ProductDetails(RetrieveUpdateDestroyAPIView):
    """ RetrieveUpdateDestroyAPIView provides a default implementation of get(), patch() and delete(). RetrieveUpdateDestroyAPIView requires two mandatory attributes which are serializer_class and queryset.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # lookup_field = 'id'

    # Our view has a very commonly occuring pattern where we want to see detail of a model instance, want to edit a model instance and delete a model instance. We had to provide a get(), patch() and delete() implementation to achieve this. But in delete method we are add one more extra condition before deleteing it so that way we are overriding the delete() implementation from RetriveUpdateDestroyAPIView class.

    def delete(self, request, pk):
        # Read the object from database using ID
        product = get_object_or_404(Product, pk=int(pk))
        if product.orderitem_set.count() > 0:
            return Response({'can not delete this product becase order item are related to it.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Generie based view


class CollectionList(ListCreateAPIView):
    """If you are not changing the serializer class based on user type then you can define this serializer class name with one line only
    """
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
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)

    if request.method == "GET":
        # Get serialize object
        serializer = CollectionSerializer(collection)

        # Return the serializer object data with status code 200
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        # De-serialize the object
        serializer = CollectionSerializer(
            data=request.data, instance=collection)

        # validate the object
        serializer.is_valid(raise_exception=True)

        serializer.save()

    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Customized Generic View
class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
