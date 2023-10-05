import os
import tempfile
from django.views import View
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.core import mail
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

        # Format email body and user
        user = users[0]
        message, subject = get_message_subject(form_data)
        
        # Get sender credentials
        if not user.email_sender:
            return JsonResponse ({
                "status": "error",
                "message": "email sender not found",
                "data": {}
            }, status=404)
        
        # Detect spam in message content
        is_spam = get_is_spam(message)

        # Get files from form and save in media
        files_paths = []
        form_files = request.FILES
        if form_files:
            for file in form_files:
                file_name = form_files[file].name
                
                # Clean file name
                replace_chars = [" ", "/", "\\", ":", "'", '"', "(", ")", "[", "]", "{", "}", "!", "?", "&", "#", "$", "%", "^", "*", "+", "=", "~", "`", "|", "<", ">"]
                for char in replace_chars:
                    file_name = file_name.replace(char, "_")
                    
                # Use a temporary directory to save the file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(form_files[file].read())
                    files_paths.append(temp_file.name)
            
        if is_spam:
            # Dont send message and change subject in history
            subject = f"Spam try in {user.name}"
        else:
            # Send email (only if not spam)
            
            # Change email credentials
            sender = user.email_sender
            connection = mail.get_connection(
                host=sender.host,
                port=sender.port,
                username=sender.username,
                password=sender.password,
                use_ssl=sender.use_ssl
            )
            connection.open ()
            
            # Create email 
            email = EmailMessage (
                subject=subject,
                body=message,
                from_email=sender.username,
                to=[user.to_email],
            )
            
            # Attach files
            for file_path in files_paths:
                email.attach_file(file_path)

            # Send email
            email.connection = connection
            email.send(
                fail_silently=False
            )
            
            connection.close ()
            
        # Save in history
        models.History.objects.create (
            user = users[0], 
            subject = subject,
            message = message,
            sent = not is_spam    
        )
        
        # Delete temporal files
        for temp_file_path in files_paths:
            os.remove(temp_file_path)
        
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