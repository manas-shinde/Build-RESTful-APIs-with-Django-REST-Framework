from django.urls import path, include
import debug_toolbar
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', viewset=views.ProductViewSet)
router.register('collections', viewset=views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(
    router, r'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet,
                        basename="product-reviews")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]
