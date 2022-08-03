from payment_info.models import PaymentInfo
from core.exceptions import ExpiredCardError, CreatePaymentInfoError
from datetime import datetime

def create_payment_info(validated_data):
    payment_info = PaymentInfo(**validated_data)
        
    # Se o cartão estiver vencido, informe uma mensagem e não deixe o cartão ser cadastrado
    if payment_info.card_expiring_date < datetime.now().date():
        raise ExpiredCardError
        
    # Verifica se o cartão já está cadastrado para esse usuário
    find_payment_method = PaymentInfo.objects.filter(
            payment_method = payment_info.payment_method,
            card_number = payment_info.card_number,
            card_expiring_date = payment_info.card_expiring_date,
            cvv = payment_info.cvv,
            customer = payment_info.customer
        ).exists()
        
    if find_payment_method:
        raise CreatePaymentInfoError
        
    payment_info.save()
        
    return payment_info