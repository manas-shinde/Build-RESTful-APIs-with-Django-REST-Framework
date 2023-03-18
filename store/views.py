from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import Order, Product, Collection, OrderItem, Review, Cart, CartItem, Customer
from .filters import ProductFilter
from .pagination import ProductPagination
from .serializers import OrderSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer
from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly

# ModelViewset


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')

# Using specific ModelMixin's becase we dont want to show all carts to every user.


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


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

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = ProductFilter

    search_fields = ['title', 'description']

    ordering_fields = ['id', 'unit_price', 'last_update']

    pagination_class = ProductPagination

    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]

    def get_permissions(self):
        """This method is used to applay sepcific validation only on sum points only.
        Like for just retriving data user not needs to be authorized but to update entites user needs to be authorized

        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection, pk=kwargs["pk"])
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()

    serializer_class = CustomerSerializer
    permission_classes = [FullDjangoModelPermissions]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, requset):
        (customer, created) = Customer.objects.get_or_create(
            user_id=requset.user.id)

        if requset.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif requset.method == "PUT":
            serializer = CustomerSerializer(customer, data=requset.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        (customer_id, is_customer_created) = Customer.objects.only(
            'id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
