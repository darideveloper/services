from django.db import models


class Credentilas(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    public_key = models.CharField(max_length=200)
    secret_key = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.public_key[0:10]}..."
    
    class Meta:
        verbose_name = "Credentials"
        verbose_name_plural = "Credentials"