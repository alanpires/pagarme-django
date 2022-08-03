from django.db import models
from transactions.models import Transaction
from fees.models import Fee
from accounts.models import User
from core.models import CleanModel
from datetime import timedelta, datetime
import uuid
import ipdb

class Payable(CleanModel):
    PAYABLE_CHOICES = (
        ('paid', 'paid'),
        ('waiting_funds', 'waiting_funds')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=13, choices=PAYABLE_CHOICES)
    payment_date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0.00)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='payable')
    fee = models.ForeignKey(Fee, on_delete=models.PROTECT, related_name='payables')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payables')
    
    def __str__(self):
        return f'{self.status}'
    
    def define_status(self):
        if self.transaction.payment_info.payment_method == 'debit':
            self.status = 'paid'
        
        elif self.transaction.payment_info.payment_method == 'credit':
            self.status = 'waiting_funds'
        
        return self.status
    
    def define_payment_date(self):
        if self.transaction.payment_info.payment_method == 'debit':
            self.payment_date = self.transaction.created_at
        
        elif self.transaction.payment_info.payment_method == 'credit':
            self.payment_date = self.transaction.created_at + timedelta(days=30)
            
        return self.payment_date
    
    def calculate_amount_client(self):
        if self.transaction.payment_info.payment_method == 'debit':
            value = float(self.transaction.amount) - (float(self.transaction.amount) * float(self.fee.debit_fee))
            self.amount = "{:.2f}".format(value)

        elif self.transaction.payment_info.payment_method == 'credit':
            value = float(self.transaction.amount) - (float(self.transaction.amount) * float(self.fee.credit_fee))
            self.amount = "{:.2f}".format(value)

        return self.amount
    
    def change_status(self):
        date = datetime.now().date()
        
        if self.payment_date < date and self.status == 'waiting_funds':
            self.status = 'paid'
        
        return self.status