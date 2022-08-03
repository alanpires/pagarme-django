from rest_framework.permissions import BasePermission
from products.models import Product
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from core.exceptions import PaymentInfoMissingException

class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        
        return bool(request.user.is_authenticated and request.user.is_admin)

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_admin)
    
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_seller)
    
class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        return bool(request.user.is_authenticated and request.user.is_seller)

class IsSellerAndProductBelognsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        
        product = get_object_or_404(Product, id=view.kwargs['product_id'])
        if request.user.is_anonymous:
            raise NotAuthenticated
        
        if product.seller == request.user:
            return bool(request.user.is_authenticated and request.user.is_seller)
        else:
            raise PermissionDenied

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_seller == False and request.user.is_admin == False)

class IsSellerToListOrIsCustomerToCreateAndPaymentInfoIdVerify(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user.is_admin or request.user.is_seller)
        
        if request.method == 'POST':
            payment_info = request.data.get('payment_info', None)
            
            if not payment_info:
                raise PaymentInfoMissingException
            
            if request.user.payment_info.filter(id=request.data.get('payment_info')['id']).exists():
                return bool(request.user.is_seller == False and request.user.is_admin == False)
            
            else:
                raise PermissionDenied
            
        return bool(request.user.is_seller)