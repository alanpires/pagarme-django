from .models import Payable
from django.db.models import Sum

class PayableService:
    def __init__(self, user):
        self.user = user
    
    payable_serializer = {}
    
    @classmethod
    def define_payable_serializer(cls, user):
        payables = Payable.objects.all()
            
        # Alterar o status de todos os payables
        for payable in payables:
            payable.change_status()
            payable.save()
            
        # Filtrar os valores de todos os payables conforme o status
        payable_amount_available = Payable.objects.filter(seller=user, status='paid').aggregate(amount_paid=Sum('amount'))
        payable_amount_waiting_funds = Payable.objects.filter(seller=user, status='waiting_funds').aggregate(amount_waiting_funds=Sum('amount'))
            
        serializer = [
            {
                "payable_amount_paid": payable_amount_available['amount_paid'],
                "payable_amount_waiting_funds": payable_amount_waiting_funds['amount_waiting_funds']
            }
        ]
            
        cls.payable_serializer = serializer
        
        return cls.payable_serializer
