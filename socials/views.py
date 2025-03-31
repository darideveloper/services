import json

from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from socials import models


@method_decorator(csrf_exempt, name='dispatch')
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
                    "video_drive_name": video.video_drive_name,
                    "description": video.description,
                    "context": video.context,
                }
            }, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "message": "No video found",
                "data": {},
            }, status=404)
    
    def post(self, request):
        
        # Get video id from request
        json_data = request.body.decode("utf-8")
        video_data = json.loads(json_data)
        video_id = video_data.get("video_id")
        
        # Get video object
        video = models.Video.objects.filter(id=video_id).first()
        
        # Check if video exists
        if not video:
            return JsonResponse({
                "status": "error",
                "message": "Video not found",
                "data": {},
            }, status=404)
        
        # Update video posted status
        video.posted = True
        video.save()
        
        return JsonResponse({
            "status": "ok",
            "message": "Video state updated",
            "data": {}
        }, status=200)
         