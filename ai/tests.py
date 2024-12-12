from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RedirectsTestCase(TestCase):
    def test_home_redirect_admin(self):
        """ Test redirect to admin when accessing the home page """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')

    def test_api_redirect_admin(self):
        """ Test redirect to admin when accessing the api page """
        response = self.client.get('/auth/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')


class ApiLoginTestView(TestCase):
    """ Test the login API view """

    def setUp(self):
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser',
            password=self.password,
            is_active=True,
        )
        self.endpoint = '/auth/login/'

    def test_invalid_missing_data(self):
        """ Test missing username and password """

        res = self.client.post(self.endpoint, data={})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Invalid data",
            "data": {
                "username": ["This field is required."],
                "password": ["This field is required."],
            }
        })

    def test_invalid_username(self):
        """ Test no registered user """

        res = self.client.post(self.endpoint, data={
            "username": "invalid",
            "password": self.user.password,
        })

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Invalid credentials",
            "data": {}
        })

    def test_invalid_password(self):
        """ Test registered user with wrong password """

        res = self.client.post(self.endpoint, data={
            "username": self.user.username,
            "password": "invalid",
        })

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Invalid credentials",
            "data": {}
        })

    def test_valid(self):
        """ Test valid user and validate generated token """
        
        res = self.client.post(self.endpoint, data={
            "username": self.user.username,
            "password": self.password,
        })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {
            "status": "success",
            "message": "User logged in",
            "data": {
                "token": self.user.auth_token.key,
                "username": self.user.username,
            }
        })


class ApiProfileTestView(TestCase):
    """ Test the profile API view """

    def setUp(self):
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username='testuser',
            password=self.password,
            email="test@gmail.com",
        )
        self.endpoint = '/auth/profile/'

    def test_invalid_token(self):
        """ Test using invalid token """

        res = self.client.get(self.endpoint, HTTP_AUTHORIZATION='Token invalid')

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Invalid token.",
            "data": {}
        })
    
    def test_missing_token(self):
        """ Test without sending token """

        res = self.client.get(self.endpoint)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json(), {
            "status": "error",
            "message": "Authentication credentials were not provided.",
            "data": {}
        })

    def test_valid(self):
        """ Test width valid token and check user data """

        token, _ = Token.objects.get_or_create(user=self.user)
        res = self.client.get(
            self.endpoint,
            HTTP_AUTHORIZATION=f'Token {token}'
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {
            "status": "success",
            "message": "User profile",
            "data": {
                "username": self.user.username,
                "email": self.user.email,
            }
        })