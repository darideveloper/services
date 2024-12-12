from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    def post(self, request):

        # Use serializer for validation
        serializer = LoginSerializer(data=request.data)
        valid_data = serializer.is_valid(raise_exception=False)
        if not valid_data:
            return Response({
                "status": "error",
                "message": "Invalid data",
                "data": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        invalid_credentials_error = {
            "status": "error",
            "message": "Invalid credentials",
            "data": {}
        }

        # # Get and validate user
        user = User.objects.filter(username=request.data['username'])
        if not user.exists():
            return Response(
                invalid_credentials_error,
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Validate password
        user = user.first()
        if not user.check_password(request.data['password']):
            return Response(
                invalid_credentials_error,
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get user token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "status": "success",
            "message": "User logged in",
            "data": {
                "token": token.key,
                "username": user.username,
            },
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get user profile
        serializer = UserSerializer(request.user)

        # Return user profile
        return Response({
            "status": "success",
            "message": "User profile",
            "data": {
                "username": serializer.data['username'],
                "email": serializer.data['email'],
            }
        }, status=status.HTTP_200_OK)
