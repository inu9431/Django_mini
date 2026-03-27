from celery import shared_task
from datetime import date, timedelta

from app.analysis.analyzer import Analyzer
from app.users.models import User

@shared_task
def run_weekly_analysis():
    today = date.today()
    period_start = today - timedelta(days=7)

    for user in User.objects.filter(is_active=True):
        analyzer = Analyzer(user, period_start, today)
        analyzer.analyze(about="주간 자동 분석", period_type="weekly")

@shared_task
def run_monthly_analysis():
    today = date.today()
    period_start = today.replace(day=1)

    for user in User.objects.filter(is_active=True):
        analyzer = Analyzer(user, period_start, today)
        analyzer.analyze(about="월간 자동 분석", period_type="monthly")