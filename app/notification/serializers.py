from rest_framework import serializers
from app.notification.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.BooleanField(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']