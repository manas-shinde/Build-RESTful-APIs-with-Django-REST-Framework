from rest_framework import serializers
from decimal import Decimal

from .models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    # Instead of defining the variable again we'll just use the ModelSerialzer class
    #  id = serializers.IntegerField()
    #  title = serializers.CharField(max_length=255)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # Instead of defining the variable again we'll just use the ModelSerialzer class

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug',
                  'unit_price', 'inventory', 'price_with_tax', 'collection']

    # change the name of field
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source="unit_price")

    # creating new field for product model
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # To print Nested collection object
    # collection = CollectionSerializer()

    # # To Print Hyperlink for collection
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'items', 'cart_items_total']

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    cart_items_total = serializers.SerializerMethodField()

    def get_cart_items_total(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
