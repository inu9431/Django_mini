import logging
from celery import shared_task
from datetime import date, timedelta

from app.analysis.analyzer import Analyzer
from app.users.models import User

logger = logging.getLogger(__name__)

@shared_task
def run_weekly_analysis():
    today = date.today()
    period_start = today - timedelta(days=7)

    for user in User.objects.filter(is_active=True):
        try:
            analyzer = Analyzer(user, period_start, today)
            analyzer.analyze(summary="주간 자동 분석", period_type="weekly")
        except Exception as e:
            logger.error(f"주간 분석 실패 user={user.id}: {e}")

@shared_task
def run_monthly_analysis():
    today = date.today()
    period_start = today.replace(day=1)

    for user in User.objects.filter(is_active=True):
        try:
            analyzer = Analyzer(user, period_start, today)
            analyzer.analyze(summary="월간 자동 분석", period_type="monthly")
        except Exception as e:
            logger.error(f"월간 분석 실패 user={user.id}: {e}")