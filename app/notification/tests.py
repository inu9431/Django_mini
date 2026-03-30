import pytest
from django.urls import reverse

from app.analysis.models import Analysis
from app.notification.models import Notification

@pytest.mark.django_db
class TestNotification:
    def test_create_notification(self, user):
        notification = Notification.objects.create(
            user=user,
            message="테스트 알림"
        )
        assert notification.is_read is False
        assert notification.user == user

    def test_signal_creates_notification(self, user):
        from datetime import date
        Analysis.objects.create(
            user=user,
            summary="테스트 분석",
            period_type="weekly",
            period_start=date.today(),
            period_end=date.today()
        )
        assert Notification.objects.filter(user=user).count() == 1

    def test_read_notification(self, user):
        notification = Notification.objects.create(
            user=user,
            message="테스트"
        )
        notification.is_read = True
        notification.save()
        assert Notification.objects.get(pk=notification.pk).is_read is True


@pytest.mark.django_db
class TestNotificationAPI:
    def test_list_unread_notifications(self, api_client, user):
        Notification.objects.create(
            user=user,
            message="읽지 않음",
        )
        Notification.objects.create(
            user=user,
            message="읽음",
            is_read=True
        )

        api_client.force_authenticate(user=user)
        response = api_client.get(reverse('notification-list'))

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_read_notification(self, api_client, user):
        notification = Notification.objects.create(
            user=user,
            message="테스트"
        )

        api_client.force_authenticate(user=user)
        response = api_client.patch(reverse('notification-read', kwargs={'pk': notification.pk}))

        assert response.status_code == 200
        assert Notification.objects.get(pk=notification.pk).is_read is True


