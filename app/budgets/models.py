from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('income', '수입'),
        ('expense', '지출'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account.name} - {self.type} - {self.amount}"