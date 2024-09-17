from django.views import View
from django.http import JsonResponse


class Index (View):

    def get(self, request):
        return JsonResponse({
            "status": "ok",
            "message": "running",
            "data": {}
        })
