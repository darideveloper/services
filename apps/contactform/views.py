from contactform import models
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from services import settings
from django.views import View
from django.utils.decorators import method_decorator

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
        message = ""
        subject = "New contact message!"
        for input_name, input_value in form_data.items():

            # Get body values
            if input_name not in ["api_key", "redirect", "subject", "user"]:
                message += f"{input_name}: {input_value}\n"

            # Get custom subject
            if input_name == "subject":
                subject = input_value

        # Detect blacklist emails in message content
        is_spam = False
        blackLiist_email_found = ""
        message_clean = message.lower().strip()
        blackLiist_emails = map (lambda elem : elem.to_email, models.BlackList.objects.all())
        for blackLiist_email in blackLiist_emails:
            blackLiist_email_clean = blackLiist_email.lower().strip()
            if blackLiist_email_clean in message_clean:
                is_spam = True
                blackLiist_email_found = blackLiist_email
                break

        if is_spam:
            # Dont send message and change subject in history
            subject = f"Spam try from {blackLiist_email_found}"
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