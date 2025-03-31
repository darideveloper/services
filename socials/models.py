from django.db import models


class Video(models.Model):
    """ Videos to posts in social media """
    
    id = models.AutoField(primary_key=True)
    video_drive_name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    context = models.TextField()
    posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.video_drive_name
    
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['-id']