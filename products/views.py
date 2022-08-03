from cgitb import lookup

from django.shortcuts import get_object_or_404
from .models import Product
from rest_framework import generics
from .serializers import ProductSerializer, ProductListSerializer
from core.permissions import IsSellerAndProductBelognsSellerOrReadOnly, IsSellerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from accounts.models import User


class ProductView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        return super().perform_create(serializer)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return super().get_serializer_class()

    
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSellerAndProductBelognsSellerOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_url_kwarg = 'product_id'

class ProductSellerView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_url_kwarg = 'seller_id'

    def get_queryset(self):
        seller = get_object_or_404(User, pk=self.kwargs['seller_id'])
        queryset = Product.objects.filter(seller=seller)
        return queryset