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
                    "video_drive_url": video.video_drive_url,
                    "posted": video.posted,
                    "workflow_link": video.workflow_link,
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
         