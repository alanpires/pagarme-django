from django.urls import path
from .views import AccountsCreateView, AccountsListView, LoginView

urlpatterns = [
    path('accounts/', AccountsCreateView.as_view()),
    path('accounts/', AccountsListView.as_view()),
    path('login/', LoginView.as_view())
]