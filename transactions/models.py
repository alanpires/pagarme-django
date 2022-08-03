from django.db import models
from django.utils import timezone
from products.models import Product
from payment_info.models import PaymentInfo
from accounts.models import User
import uuid

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(Product, through='Order')
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.PROTECT, related_name='transaction')
    amount = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transaction')
    created_at = models.DateField(auto_now_add=True)
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    quantity = models.IntegerField()
    amount = models.FloatField()