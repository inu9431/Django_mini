from django.urls import path
from .views import AccountListView, AccountDetailView, TransactionListView, TransactionDetailView

urlpatterns = [
    path('accounts/', AccountListView.as_view()),
    path('accounts/<int:pk>/', AccountDetailView.as_view()),
    path("transactions/", TransactionListView.as_view()),
    path("transactions/<int:pk>/", TransactionDetailView.as_view()),
]
