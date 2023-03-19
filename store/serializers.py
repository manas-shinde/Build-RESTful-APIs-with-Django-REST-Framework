from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem, Product, Collection, Review, Cart, CartItem, Customer


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
    items = CartItemSerializer(many=True, read_only=True)
    cart_items_total = serializers.SerializerMethodField()

    def get_cart_items_total(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, data):
        if not Product.objects.filter(pk=data).exists():
            raise serializers.ValidationError(
                f"No product with the given ID {data} present in databases.")
        return data

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        field = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            # Performating these saving and updating database values with transction object means either all operations will perform or not
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']

            (customer, is_customer_created) = Customer.objects.get_or_create(
                user_id=self.context['user_id'])

            order = Order.objects.create(customer=customer)
            # TODO : save the order item

            cart_items = CartItem.objects.select_related(
                'product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
