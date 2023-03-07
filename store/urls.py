from django.urls import path, include
import debug_toolbar
from . import views


urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collections/<int:pk>', views.collection_details,
         name='collection-detail')
]
