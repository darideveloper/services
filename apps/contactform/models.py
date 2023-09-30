from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField (max_length=100)
    api_key = models.CharField (max_length=32)
    to_email = models.CharField (max_length=250)

    def __str__ (self):
        return self.name

class History (models.Model):
    datetime = models.DateTimeField (auto_now_add=True)
    user = models.ForeignKey (User, on_delete=models.SET_NULL, null=True)
    subject = models.CharField (max_length=250, default=None)
    message = models.TextField (default=None)
    sent = models.BooleanField (default=False)

    def __str__ (self):
        return f"{self.datetime} {self.user.name} {self.subject}"
