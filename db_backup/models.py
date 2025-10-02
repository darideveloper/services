from django.db import models


class Credentials(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    database = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.host}:{self.port} - {self.database}"
    
    class Meta:
        verbose_name = "Credentials"
        verbose_name_plural = "Credentials"


class Backup(models.Model):
    id = models.AutoField(primary_key=True)
    credentials = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    backup_file = models.FileField(upload_to="backups/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.credentials.username} - {self.backup_file.name}"
    
    class Meta:
        verbose_name = "Backup"
        verbose_name_plural = "Backups"