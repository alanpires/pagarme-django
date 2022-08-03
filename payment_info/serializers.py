from rest_framework import serializers
from payment_info.services import create_payment_info
from .models import PaymentInfo

class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = '__all__'
        extra_kwargs = {'is_active': {'read_only': True}, 
                        'customer': {'read_only': True}, 
                        'cvv': {'write_only': True}, 
                        'card_number': {'write_only': True}}

    card_number_info = serializers.SerializerMethodField()
    
    def get_card_number_info(self, obj):
        return obj.card_number[-4:]
    
    def create(self, validated_data):      
        payment_info = create_payment_info(validated_data)
        
        return payment_info