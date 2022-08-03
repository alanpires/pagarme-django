from django.core.exceptions import ObjectDoesNotExist
from core.exceptions import ProductsFromDifferentSellersAndDoesNotExistAndNotAvailableAndIsNotActiveError
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from payment_info.models import PaymentInfo
from core.exceptions import ExpiredCardError
from transactions.models import Transaction
from transactions.models import Order
from django.db.models import Sum
from payables.models import Payable
import ipdb

class TransactionService:
    def __init__(self, seller_id, products, payment_info):
        self.seller_id = seller_id
        self.products = products
        self.payment_info = payment_info
    
    all_products = []
    transaction = {}
    
    @staticmethod
    def verify_product_seller_quantity(seller_id, products):
        for product in products:
            try:
                Product.objects.get(seller_id=seller_id, id=product['id'], quantity__gte=product['quantity'], is_active=True)

            except ObjectDoesNotExist:
                raise ProductsFromDifferentSellersAndDoesNotExistAndNotAvailableAndIsNotActiveError
            
            if product['quantity'] <= 0:
                raise ProductsFromDifferentSellersAndDoesNotExistAndNotAvailableAndIsNotActiveError 
    
    @staticmethod        
    def verify_expired_card(payment_info):
        payment_info = PaymentInfo.objects.get(id=payment_info['id'])
        payment_info.define_is_active()
        payment_info.save()
        
        if payment_info.is_active == False:
            raise ExpiredCardError  
    
    def keep_all_products(self, products):
        products_list = []
        
        for product in products:
            find_product = Product.objects.get(id=product['id'])
            product_data = {
                "product": find_product,
                "quantity": product['quantity']
            }
            products_list.append(product_data)

        self.all_products = products_list    

    def create_transaction(self, seller_id, payment_info):
        transaction = Transaction.objects.create(
        seller_id = seller_id,
        payment_info_id = payment_info['id']
        )

        self.transaction = transaction   

    def create_orders_and_decrease_products_seller(self):
        for product in self.all_products:      
            amount = product['product'].price * product['quantity']
            Order.objects.create(transaction=self.transaction, 
                                 product=product['product'],
                                 quantity=product['quantity'],
                                 amount=amount
                                 )
            product['product'].quantity -= product['quantity']
            product['product'].save()

        sum_amount_orders = Order.objects.filter(transaction=self.transaction).aggregate(amount=Sum('amount'))
        self.transaction.amount = sum_amount_orders['amount']
       
        self.transaction.save()    

    def create_payable(self, fee, seller_id):
        payable = Payable(
        transaction=self.transaction,
        fee=fee,
        seller_id=seller_id
        )
        payable.define_status()
        payable.define_payment_date()
        payable.calculate_amount_client()
        payable.save()

    def return_transaction(self):
        return self.transaction