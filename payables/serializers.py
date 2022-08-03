from rest_framework import serializers
from .models import Payable
from django.db.models import Sum
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import OpenApiExample

class PayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payable
        fields = '__all__'

@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Payables',
            value={
                'payable_amount_paid': 575.98,
                'payable_amount_waiting_funds': 284.99
            },
            response_only=True,
        )
    ]
)
class PayableDocSerializer(serializers.Serializer):
    payable_amount_paid= serializers.DecimalField(max_digits=19, decimal_places=2)
    payable_amount_waiting_funds= serializers.DecimalField(max_digits=19, decimal_places=2)

    