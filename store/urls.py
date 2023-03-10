from django.urls import path, include
import debug_toolbar
from . import views


urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<int:pk>/', views.ProductDetails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>', views.CollectionDetails.as_view())
]
