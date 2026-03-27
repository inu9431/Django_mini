from django.db import models
from django.conf import settings

class Analysis(models.Model):
    PERIOD_TYPE = [
        ("weekly", " 주간"),
        ("monthly", " 월간")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=PERIOD_TYPE)
    period_start = models.DateField()
    period_end = models.DateField()
    description = models.TextField(blank=True)
    result_image = models.ImageField(upload_to='analysis/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.period_start}"
