from .models import Fee
from rest_framework import generics
from .serializers import FeeSerializer
from core.permissions import IsAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class FeeView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    
class FeeRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    lookup_url_kwarg = 'fee_id'