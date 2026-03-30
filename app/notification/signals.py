from django.db.models.signals import post_save
from django.dispatch import receiver

from app.analysis.models import Analysis
from app.notification.models import Notification

@receiver(post_save, sender=Analysis)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"새로운 분석 결과가 생성됬습니다: {instance.summary}",
        )