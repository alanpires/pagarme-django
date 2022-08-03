from django.db import models
from accounts.models import User
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='products')