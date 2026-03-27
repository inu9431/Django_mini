from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'balance', 'created_at')
        read_only_fields = ('created_at',)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'type','account','description','date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at',)