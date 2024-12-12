import json

from openai import OpenAI

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from ai import models


@method_decorator(csrf_exempt, name='dispatch')
class Index (APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """ Send data to huggingface model and return response """
                
        # Get json data
        json_data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ["text"]
        for field in required_fields:
            if not json_data.get(field) or not json_data.get(field):
                return JsonResponse({
                    "status": "error",
                    "message": f"missing {field} input",
                    "data": {}
                }, status=400)
        
        # Get model and text
        text = json_data.get("text")
        user = models.User.objects.filter(name="daridev_rrss").first()
        
        # get response from huggingface model
        client = OpenAI(
            api_key=user.api_key
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": user.prompt,
                },
                {
                    "role": "user",
                    "content": text,
                }
            ]
        )

        response = completion.choices[0].message.content
        return JsonResponse({
            "status": "success",
            "message": "response from huggingface model",
            "data": {
                "response": response
            }
        }, status=200)
                        
                
        
        
        