from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=250)
    prompt = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"