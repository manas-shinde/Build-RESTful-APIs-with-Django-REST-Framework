from django.urls import path, include
import debug_toolbar
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', viewset=views.ProductViewSet, basename='products')
router.register('collections', viewset=views.CollectionViewSet)
router.register('carts', views.CartViewSet)

product_router = routers.NestedDefaultRouter(
    router, r'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet,
                        basename="product-reviews")

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(carts_router.urls)),
    path('', include(product_router.urls))
]
