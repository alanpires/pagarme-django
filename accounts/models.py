from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from core.models import CleanModel
import uuid

class CustomUserManager(BaseUserManager):
    """
    Estamos modificando o comportamento da função que 
    faz a criação de usuários, para que os usuários sejam 
    criados com email e senha.
    """
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        
        # Caso não seja fornecido um email, estoure uma excessão
        if not email:
            raise ValueError('The given email must be set')
        
        # Essa função coloca em letras minúsculas a 
        # parte do domínio do email para evitar variantes do mesmo e-mail
        email = self.normalize_email(email)
        
        # Aqui estamos setando os valores 
        # padrões para os campos padrões do User
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)

        # Fazendo o hash de senha
        user.set_password(password)

        # Salvando as informações no banco de dados
        user.save(using=self._db)

        return user
        
    # Agora nossos método create_user e 
    # create_superuser não necessitam mais de username
    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                         **extra_fields)
        
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                     **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    is_seller = models.BooleanField()
    is_admin = models.BooleanField()
    username = models.CharField(max_length=255, unique=False, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name} - {self.email}'
    
