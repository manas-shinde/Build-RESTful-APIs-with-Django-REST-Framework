from django.urls import path, include
import debug_toolbar
from . import views


urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<int:id>/', views.ProductDetails.as_view()),
    path('collections/', view=views.CollectionList.as_view()),
    path('collections/<int:pk>', views.collection_details,
         name='collection-detail')
]
