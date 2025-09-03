from django.db import models


class Activity(models.Model):
    ORIGINS_OPTIONS = [
        ('lite', 'Linux Lite'),
        ('windows', 'Windows'),
    ]
    origin = models.CharField(max_length=255, choices=ORIGINS_OPTIONS)
    json_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Activity from {self.origin} at {self.created_at}"
