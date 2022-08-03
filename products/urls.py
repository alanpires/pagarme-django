from django.urls import path
from .views import ProductRetrieveUpdateDestroyView, ProductSellerView, ProductView

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('products/<str:product_id>/', ProductRetrieveUpdateDestroyView.as_view()),
    path('products/seller/<str:seller_id>/', ProductSellerView.as_view())
]