from rest_framework import serializers
from .models import Product
from accounts.serializers import UserSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    seller = UserSerializer(read_only=True)
    quantity = serializers.IntegerField(min_value=0)
    
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'seller': {'read_only': True}}