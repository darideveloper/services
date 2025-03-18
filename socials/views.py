from django.views import View
from django.http import JsonResponse

from socials import models


class VideoView(View):
    
    def get(self, request):
        
        # Get older video no posted
        video = models.Video.objects.filter(posted=False).first()
        
        # Return video data
        if video:
            return JsonResponse({
                "status": "ok",
                "message": "Video data",
                "data": {
                    "title": video.title,
                    "description": video.description,
                    "tags": video.tags,
                    "file_s3_url": video.file_s3_url,
                    "posted": video.posted,
                    "odoo_task": video.odoo_task,
                    "created_at": video.created_at,
                    "updated_at": video.updated_at,
                }
            }, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "message": "No video found",
                "data": {},
            }, status=404)
         