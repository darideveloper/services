import os

import requests

from contactform import models

from django.core.management.base import BaseCommand
from django.conf import settings


BASE_FILE = os.path.basename(__file__)

SUBJECT = "test periodic contact form"
MESSAGE = "periodic contact form test message"
HISTORY_OBJECTS_INITIAL = models.History.objects.all()
INITIAL_EMAILS = HISTORY_OBJECTS_INITIAL.count()


class Command(BaseCommand):
    help = "Generate next report ready to be processed"

    def validate_email_sent(self, res: requests.Response, total_emails: int):
        """Validate email sent from api response and database

        Args:
            res (requests.Response): API response
            total_emails (int): Total emails sent
        """

        assert res.status_code == 200
        assert res.json()["status"] == "success"
        assert res.json()["message"] == "email sent"
        assert res.json()["data"] == {}

        # Validate email sent in database
        history_objects = models.History.objects.all().order_by("-datetime")
        assert history_objects.count() - INITIAL_EMAILS == total_emails
        assert history_objects[0].subject == SUBJECT
        assert MESSAGE in history_objects[0].message
        assert history_objects[0].sent is True
        
        print(f"Test email {total_emails} sent")
        
    def handle(self, *args, **kwargs):

        # Calculate endpoint
        endpoint = f"{settings.HOST}/contact-form/"

        credentials = [
            {
                "user": settings.TEST_DARIDEV_USER,
                "api_key": settings.TEST_DARIDEV_API_KEY,
                "use_file": False,
            },
            {
                "user": settings.TEST_CAKES_USER,
                "api_key": settings.TEST_CAKES_API_KEY,
                "use_file": True,
            },
        ]

        for credential in credentials:

            # data
            form_data = {
                "name": "test name",
                "email": "test@test.com",
                "subject": SUBJECT,
                "message": MESSAGE,
                "user": credential["user"],
                "api_key": credential["api_key"]
            }
            form_file = {
                "file": open(
                    os.path.join(settings.BASE_DIR, "media", "test.webp"), "rb"
                )
            }

            # submit contact form
            res = requests.post(
                endpoint,
                data=form_data if credential["use_file"] else None,
                files=form_file if credential["use_file"] else None,
                json=form_data if not credential["use_file"] else None,
            )
            
            # Validate response
            total_emails = credentials.index(credential) + 1
            self.validate_email_sent(res, total_emails)
