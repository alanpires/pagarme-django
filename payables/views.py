from rest_framework import generics
from core.permissions import IsSeller
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Payable
from .serializers import PayableSerializer
from rest_framework.response import Response
from .services import PayableService
from drf_spectacular.utils import extend_schema
from .serializers import PayableDocSerializer

@extend_schema(
    responses={200: PayableDocSerializer(many=False)},
)
class PayableView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSeller]
    queryset = Payable.objects.all()
    serializer_class = PayableSerializer
    
    def list(self, request, *args, **kwargs):
        serializer = PayableService.define_payable_serializer(request.user)
        
        return Response(serializer)