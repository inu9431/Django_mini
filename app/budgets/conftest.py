import pytest
from app.budgets.models import Account, Transaction

@pytest.fixture
def account(user):
    return Account.objects.create(user=user, name='테스트 계좌', balance=10000)

@pytest.fixture
def transaction(account):
    return Transaction.objects.create(
        account=account, transaction_type="expense", amount=3000, date="2026-03-25"
    )