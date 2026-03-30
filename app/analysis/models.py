from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Analysis(models.Model):
    PERIOD_TYPE = [
        ("weekly", "주간"),
        ("monthly", "월간")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255)
    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE, default="monthly")
    period_start = models.DateField()
    period_end = models.DateField()
    description = models.TextField(blank=True)
    result_image = models.ImageField(upload_to='analysis/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.period_type} - {self.period_start}"

    def clean(self):
        if self.period_start and self.period_end:
            if self.period_start > self.period_end:
                raise ValidationError("종료일은 시작일 보다 앞일수 없습니다")