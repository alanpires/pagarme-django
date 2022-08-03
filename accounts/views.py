import drf_spectacular
from .models import User
from .serializers import TokenSerializer, UserSerializer, LoginSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from core.permissions import IsAdminOrCreateOnly
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema
from .serializers import TokenSerializer

@extend_schema(
    auth=[]
)
class AccountsCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountsListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrCreateOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@extend_schema(
    auth=[],
    responses=TokenSerializer
)  
class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=serializer.validated_data['email'], 
                            password=serializer.validated_data['password'])
        
        if user is not None:
            # Aqui fazemos a criação do Token e o vinculamos ao usuário
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token': token.key})
    
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
