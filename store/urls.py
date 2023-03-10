from django.urls import path, include
import debug_toolbar
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', viewset=views.ProductViewSet)
router.register('collections', viewset=views.CollectionViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('products/', views.ProductsList.as_view()),
    # path('products/<int:pk>/', views.ProductDetails.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>', views.CollectionDetails.as_view())
]
