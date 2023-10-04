from django.views import View
from django.shortcuts import render
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from services import settings
from contactform import models
from core.utils import get_is_spam, get_message_subject


@method_decorator(csrf_exempt, name='dispatch')
class Index (View):
    
    def post (self, request):
        """ Send email and redirect """

        # Get form data
        form_data = request.POST.dict()

        # Check all inputs
        inputs_names = ["api_key", "user"]
        for input_name in inputs_names:
            if input_name not in form_data.keys():
                return JsonResponse ({
                    "status": "error",
                    "message": f"missing {input_name} input",
                    "data": {}
                }, status=400)

        # Validate api user name
        valid_login = False
        users = models.User.objects.filter (name=form_data["user"])
        if users and users[0].api_key == form_data["api_key"]:
            valid_login = True

        # Return login error
        if not valid_login:
            return JsonResponse ({
                "status": "error",
                "message": "invalid login",
                "data": {}
            }, status=401)

        # Format email body
        message, subject = get_message_subject(form_data)
        
        # Detect spam in message content
        is_spam = get_is_spam(message)

        # Get files from form

        if is_spam:
            # Dont send message and change subject in history
            subject = f"Spam try in {users[0].name}"
        else:
            # Send email 
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [users[0].to_email],
                fail_silently=False,
            )

        # Save in history
        models.History.objects.create (
            user = users[0], 
            subject = subject,
            message = message,
            sent = not is_spam    
        )
        
        # Redirect or send response
        redirect = form_data.get("redirect", "")
        if redirect:
            return HttpResponseRedirect(form_data["redirect"]) 
        else:
            return JsonResponse ({
                "status": "success",
                "message": f"email sent",
                "data": {}
            }, status=200)
            
class TestFormFile (View):
    
    def get (self, request):
        """ Render html with form, with input file, for testing """
        
        return render (request, "contactform/test_form_file.html", {})