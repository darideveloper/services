from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Activity


@method_decorator(csrf_exempt, name="dispatch")
class ActivityWatchView(View):
    """
    View to handle POST requests to /activity-watch/{origin-key}/
    Accepts JSON data and saves it to the Activity model
    """

    def post(self, request, origin_key):
        try:
            # Validate origin_key against available choices
            valid_origins = [choice[0] for choice in Activity.ORIGINS_OPTIONS]
            if origin_key not in valid_origins:
                error_message = "Invalid origin."
                error_message += f" Must be one of: {', '.join(valid_origins)}"
                return JsonResponse(
                    {
                        "error": error_message,
                    },
                    status=400,
                )

            # Parse JSON data from request body
            try:
                json_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            # Create and save the Activity instance
            activity = Activity.objects.create(origin=origin_key, json_data=json_data)

            return JsonResponse(
                {
                    "success": True,
                    "id": activity.id,
                    "origin": activity.origin,
                    "created_at": activity.created_at.isoformat(),
                    "message": "Activity data saved successfully",
                },
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    def get(self, request, origin_key):
        try:
            activities = Activity.objects.filter(origin=origin_key)
            return JsonResponse(
                {"activities": [activity.json_data for activity in activities]},
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)