from django.urls import path
from .views import PaymentInfoView

urlpatterns = [
    path('payment_info/', PaymentInfoView.as_view()),
    # path('payment_info/<str:payment_info_id>/', PaymentInfoDeleteView.as_view())
]