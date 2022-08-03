from django.db import models
from core.models import CleanModel
import uuid
from accounts.models import User
from datetime import datetime

class PaymentInfo(CleanModel):
    PAYMENT_CHOICES = (
        ('debit', 'debit'),
        ('credit', 'credit')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_CHOICES)
    card_number = models.CharField(max_length=16)
    cardholders_name = models.CharField(max_length=30)
    card_expiring_date = models.DateField()
    cvv = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_info')
    
    def __str__(self):
        return f'{self.id} - {self.payment_method}'
    
    def define_is_active(self):
        date = datetime.now().date()
        if self.card_expiring_date < date:
            self.is_active = False
        else:
            self.is_active = True
        
        return self.is_active