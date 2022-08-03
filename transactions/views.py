from rest_framework import generics
from core.permissions import IsSellerToListOrIsCustomerToCreateAndPaymentInfoIdVerify
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer, TransactionDocSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=TransactionDocSerializer,
)
class TransactionView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSellerToListOrIsCustomerToCreateAndPaymentInfoIdVerify]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        if self.request.user.is_admin:
            queryset = Transaction.objects.all()
            return queryset
        else:
            queryset = Transaction.objects.filter(seller=self.request.user)
            return queryset