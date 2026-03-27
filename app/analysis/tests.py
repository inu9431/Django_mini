import pytest
from datetime import date
from unittest.mock import patch
from django.core.files.base import ContentFile
from app.analysis.models import Analysis
from app.analysis.analyzer import Analyzer
from app.budgets.models import Account, Transaction

@pytest.fixture
def account(user):
    return Account.objects.create(user=user, name="테스트 계좌", balance=10000)

@pytest.fixture
def transaction(account):
    return Transaction.objects.create(account=account, type="income", amount=1000, date='2026-03-20')

class TestAnalyzer:
    def test_get_dataframe(self, user, transaction):
        analyzer = Analyzer(user, date(2026, 3, 1), date(2026,3 ,21))
        df = analyzer.get_dataframe()
        assert not df.empty
        assert list(df.columns) == ['date', 'type', 'amount']

    def test_get_dataframe_empty(self, user):
        analyzer = Analyzer(user, date(2026, 1, 1), date(2026, 1, 31))
        df = analyzer.get_dataframe()
        assert df.empty

    def test_generate_image_returns_none_when_no_data(self, user):
        analyzer = Analyzer(user, date(2026, 3, 1), date(2026, 3, 31))
        result = analyzer.generate_image()
        assert result is None

    def test_analyze_creates_analysis(self, user, transaction):
        analyzer = Analyzer(user, date(2026, 3, 1), date(2026, 3, 31))
        analysis = analyzer.analyze(about="3월 분석", period_type='monthly')
        assert Analysis.objects.filter(user=user).count() == 1
        assert analysis.type == 'monthly'
        assert analysis.result_image

class TestAnalysisAPI:
    def test_list(self, auth_client, user):
        Analysis.objects.create(user=user, about="테스트", type="income", period_start=date(2026, 3, 1), period_end=date(2026, 3, 7)
                                )
        res = auth_client.get('/api/analysis/')
        assert res.status_code == 200
        assert len(res.data) == 1

    def test_filter_by_type(self, auth_client, user):
        Analysis.objects.create(
            user=user, about='주간', type='weekly',
            period_start=date(2026, 3, 1), period_end=date(2026, 3, 31)
        )
        Analysis.objects.create(
            user=user, about='월간', type='monthly',
            period_start=date(2026, 3, 1), period_end=date(2026, 3, 31)
        )
        res = auth_client.get('/api/analysis/?type=weekly')
        assert res.status_code == 200
        assert len(res.data) == 1
        assert res.data[0]['type'] == 'weekly'

    def test_only_own_analysis(self, auth_client, user):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        other = User.objects.create_user(
            email = 'other@1.com', password = 'pass', name = 'other', phone = '123'
        )
        Analysis.objects.create(
            user=other, about='남의 분석', type='weekly',
            period_start=date(2026, 3, 1), period_end=date(2026, 3, 31)
        )
        res = auth_client.get('/api/analysis/')
        assert res.status_code == 200
        assert len(res.data) == 0