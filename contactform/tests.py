from django.test import TestCase
from django.urls import reverse
from contactform import models
from utils.mails import get_message_subject


class TestViews (TestCase):

    def setUp(self):

        # Create users
        self.sender = models.EmailSender.objects.create(
            host="sample host",
            port=1234,
            username="sample username",
            password="sample password",
        )

        self.user = models.User.objects.create(
            name="test",
            api_key="test",
            to_email="sample@gmail.com",
            email_sender=self.sender
        )

        # Default email info
        self.default_info = {
            "user": self.user.name,
            "api_key": self.user.api_key,
            "subject": "test black list",
            "redirect": "http://www.google.com",
            "sample input": "sample value",
        }

    def test_spam(self):
        """ Try to send a message with a spam text
            Expected: regular response without sending email
        """

        # Add blocked email to form data and send request
        self.default_info["sample input"] = "buy now in https://www.google.com"
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate redirect
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.default_info["redirect"])

        # Get message from inputs
        message, _ = get_message_subject(self.default_info)

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 1)
        self.assertEqual(history_objects[0].user, self.user)
        self.assertEqual(history_objects[0].subject, f"Spam try in {
                         self.user.name}")
        self.assertEqual(history_objects[0].message, message)
        self.assertEqual(history_objects[0].sent, False)

    def test_no_sender(self):
        """ Try to send email with sender no registered
            Expected: error response
        """

        self.sender.delete()

        # Send request
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json()["status"], "error")
        self.assertEqual(res.json()["message"], "email sender not found")
        self.assertEqual(res.json()["data"], {})

    def test_invalid_api_key(self):
        """ Try to send a message with a invalid api key
            Expected: error response
        """

        # Change api key and send request
        self.default_info["api_key"] = "invalid"
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate response
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["status"], "error")
        self.assertEqual(res.json()["message"], "invalid login")
        self.assertEqual(res.json()["data"], {})

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 0)

    def test_invalid_user(self):
        """ Try to send a message with a invalid user
            Expected: error response
        """

        # Change user and send request
        self.default_info["user"] = "invalid"
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate response
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["status"], "error")
        self.assertEqual(res.json()["message"], "invalid login")
        self.assertEqual(res.json()["data"], {})

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 0)

    def test_missing_api_key(self):
        """ Try to send a message without api key
            Expected: error response
        """

        # Remove api key and send request
        del self.default_info["api_key"]
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate response
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["status"], "error")
        self.assertEqual(res.json()["message"], "missing api_key input")
        self.assertEqual(res.json()["data"], {})

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 0)

    def test_missing_subject(self):
        """ Try to send a message without subject
            Expected: regular response
        """

        # Remove subject and send request
        del self.default_info["subject"]
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate redirect
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.default_info["redirect"])

        message, subject = get_message_subject(self.default_info)

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 1)
        self.assertEqual(history_objects[0].user, self.user)
        self.assertEqual(history_objects[0].subject, subject)
        self.assertEqual(history_objects[0].message, message)
        self.assertEqual(history_objects[0].sent, True)

    def test_missing_user(self):
        """ Try to send a message without user
            Expected: error response
        """

        # Remove user and send request
        del self.default_info["user"]
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate response
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["status"], "error")
        self.assertEqual(res.json()["message"], "missing user input")
        self.assertEqual(res.json()["data"], {})

        # Validate info in models
        history_objects = models.History.objects.all()
        self.assertEqual(history_objects.count(), 0)

    def test_success_redirect(self):
        """ Try to send a message with all inputs
            Expected: redirect response
        """

        # Send request
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate redirect
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, self.default_info["redirect"])

    def test_success_response(self):
        """ Try to send a message with all inputs
            Expected: regular response
        """

        # Delete redirect and send request
        del self.default_info["redirect"]
        res = self.client.post(
            reverse("contactform_endpoint"),
            self.default_info
        )

        # Validate redirect
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")
        self.assertEqual(res.json()["message"], "email sent")
        self.assertEqual(res.json()["data"], {})
