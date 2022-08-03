from django.urls import path
from .views import FeeRetrieveView, FeeView

urlpatterns = [
    path('fee/', FeeView.as_view()),
    path('fee/<str:fee_id>/', FeeRetrieveView.as_view())
]