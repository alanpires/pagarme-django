from rest_framework import generics
from core.permissions import IsCustomer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import PaymentInfo
from .serializers import PaymentInfoSerializer

class PaymentInfoView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]
    queryset = PaymentInfo.objects.all()
    serializer_class = PaymentInfoSerializer
    
    def perform_create(self, serializer):
        serializer = serializer.save(customer=self.request.user)
        return serializer
    
    def get_queryset(self):
        queryset = PaymentInfo.objects.filter(customer=self.request.user)
        return queryset