from rest_framework import generics
from rest_framework.generics import get_object_or_404

from app.notification.models import Notification
from app.notification.serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)

class NotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    http_method_names = ['patch']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(is_read=True)
