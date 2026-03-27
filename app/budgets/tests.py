import pytest
from rest_framework.test import APIClient
from app.budgets.models import Account, Transaction

@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

class TestAccount:
    def test_create(self, account):
        assert account.id is not None
        assert account.name == "테스트 계좌"

    def test_read(self, account):
        found = Account.objects.get(pk=account.pk)
        assert found.name == account.name

    def test_delete(self, account):
        pk = account.pk
        account.delete()
        assert not Account.objects.filter(pk=pk).exists()

class TestTransaction:
    def test_create(self, account):
        tx = Transaction.objects.create(
            account=account, type="income", amount=5000, date="2026-03-25"
        )
        assert tx.id is not None

    def test_read(self, transaction):
        assert Transaction.objects.filter(account_id=transaction.account_id).count() == 1

    def test_update(self, account):
        tx = Transaction.objects.create(
            account=account, type="income", amount=5000, date="2026-03-25"
        )
        tx.amount = 9000
        tx.save()
        assert Transaction.objects.get(pk=tx.pk).amount == 9000

    def test_delete(self, account):
        tx = Transaction.objects.create(
            account=account, type="income", amount=5000, date="2026-03-25"
        )
        pk = tx.pk
        tx.delete()
        assert not Transaction.objects.filter(pk=pk).exists()



class TresAccountAPI:
    def test_create(self, auth_client):
        res = auth_client.post("/api/budgets/accounts",{"name": "새계좌", "balance": 5000})
        assert res.status_code == 201

    def test_list(self, auth_client, account):
        res = auth_client.get("/api/budgets/accounts/")
        res = auth_client.get("/api/budgets/accounts/")
        assert res.status_code == 200
        assert len(res.data) == 1

    def test_delete(self, auth_client, account):
        res = auth_client.delete(f"/api/budgets/accounts/{account.pk}/")
        assert res.status_code == 200

class TestTransactionAPI:
    def test_create(self, auth_client, account):
        res = auth_client.post("/api/budgets/transactions/", {
            "account": account.pk,
            "type": "income",
            "amount": 5000,
            "date": "2026-03-25",
        })
        assert res.status_code == 201

    def test_list(self, auth_client, transaction):
        res = auth_client.get("/api/budgets/transactions/")
        assert res.status_code == 200
        assert len(res.data) == 1

    def test_update(self, auth_client, transaction):
        res = auth_client.patch(f"/api/budgets/transactions/{transaction.pk}/", {
            "amount": 9000
        })
        assert res.status_code == 200
        assert res.data["amount"] == "9000.00"

    def test_delete(self, auth_client, transaction):
        res = auth_client.delete(f"/api/budgets/transactions/{transaction.pk}/")
        assert res.status_code == 204