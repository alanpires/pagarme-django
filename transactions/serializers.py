from rest_framework import serializers
from .models import Transaction
from fees.models import Fee
from .services import TransactionService
from products.models import Product
from payment_info.models import PaymentInfo
from accounts.models import User
import ipdb


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'quantity']
        extra_kwargs = {'id': {'read_only': False}}

    quantity = serializers.IntegerField(min_value=0)


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = ['id']
        extra_kwargs = {'id': {'read_only': False}}
        

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'products']
        extra_kwargs = {'id': {'read_only': False}}
    
    products = ProductSerializer(many=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'seller', 'payment_info', 'amount']
        extra_kwargs = {'amount': {'read_only': True}}
    
    seller = SellerSerializer(write_only=True)
    payment_info = PaymentInfoSerializer(write_only=True)
    
    def create(self, validated_data):
        seller_id = validated_data['seller']['id']
        products = validated_data['seller']['products']
        payment_info = validated_data['payment_info']
        
        transaction_service = TransactionService(seller_id, products, payment_info)
        
        # Todos os produtos pertencem ao mesmo vendedor, existem e se a quantidade solicitada está disponível
        transaction_service.verify_product_seller_quantity(seller_id, products)
        
        # Verificando se o cartão está vencido:
        transaction_service.verify_expired_card(payment_info)
        
        # Salvando todos os produtos em um array products
        transaction_service.keep_all_products(products)
        
        # Criando a transação
        transaction_service.create_transaction(seller_id, payment_info)
        
        # Criando as ordens e subtraindo os produtos comprados
        transaction_service.create_orders_and_decrease_products_seller()
        
        # Busca a última taxa
        fee = Fee.objects.last()

        # Criando o payable
        transaction_service.create_payable(fee, seller_id)
        
        transaction = transaction_service.return_transaction()
        
        return transaction

# Serializers criados para facilitar a documentação com drf_spectacular
class ProductsDocSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    quantity = serializers.IntegerField()

class PaymentInfoDocSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class SellerDocSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    products = ProductsDocSerializer(many=True)

class TransactionDocSerializer(serializers.Serializer):
    seller = SellerDocSerializer()    
    payment_info = PaymentInfoDocSerializer()