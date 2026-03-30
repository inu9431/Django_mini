from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'balance', 'created_at')
        read_only_fields = ('balance', 'created_at',)

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), source='account', write_only=True
    )
    class Meta:
        model = Transaction
        fields = ('id', 'account_id', 'account', 'transaction_type', 'amount', 'description', 'date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at',)

    def validate(self, data):
        request = self.context.get('request')
        account = data.get('account')
        if account and request and account.user != request.user:
            raise serializers.ValidationError("본인 계좌에만 거래내역을 추가할수 있습니다")
        return data

