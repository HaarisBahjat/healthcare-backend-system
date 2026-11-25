"""
accounts/views.py — Authentication API Views

Views handle the business logic for each API endpoint:
- RegisterView: Creates new user accounts.
- LoginView: Authenticates users and returns JWT tokens.

Why class-based views (CBVs)?
- DRF's generic views and viewsets provide built-in request parsing,
  response formatting, permission checking, and error handling.
- Reduces boilerplate compared to function-based views.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/

    Register a new user with name, email, and password.

    Why CreateAPIView?
    - It's a generic DRF view that handles POST requests for creating objects.
    - Automatically calls serializer.is_valid() and serializer.save().
    - Returns 201 Created on success with the serialized data.

    Why AllowAny permission?
    - Registration must be accessible to unauthenticated users (they don't
      have an account yet!). Our default permission is IsAuthenticated,
      so we explicitly override it here.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # Override the default IsAuthenticated permission — anyone can register
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Override create() to customize the response format.

        Why override?
        - The default CreateAPIView returns just the serialized object.
        - We want a structured response with a success message and user data,
          making the API more informative for frontend developers.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Returns 400 with errors if invalid
        user = serializer.save()

        return Response({
            'success': True,
            'message': 'User registered successfully.',
            'data': {
                'user': UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that adds user data to the token response.

    Why customize?
    - The default TokenObtainPairSerializer only returns:
      { "access": "...", "refresh": "..." }
    - We want to also include user profile information so the frontend
      doesn't need a separate API call to fetch user details after login.

    How SimpleJWT authentication works:
    1. User sends email + password to /api/auth/login/.
    2. SimpleJWT validates credentials against the database.
    3. If valid, it generates two tokens:
       - Access Token: Short-lived (60 min), sent with every API request.
       - Refresh Token: Long-lived (1 day), used to get new access tokens.
    4. Tokens are signed with SECRET_KEY using HS256 algorithm.
    """

    def validate(self, attrs):
        """
        Override validate() to append user data to the token response.

        The parent's validate() method:
        1. Authenticates the user (checks email + password).
        2. Generates access and refresh tokens.
        3. Returns {'access': '...', 'refresh': '...'}.

        We call super().validate() first to get the tokens, then add user info.
        """
        # Get the default token data (access + refresh tokens)
        data = super().validate(attrs)

        # Append user profile data to the response
        data['user'] = UserSerializer(self.user).data

        return data


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/

    Authenticate a user and return JWT tokens + user data.

    Why extend TokenObtainPairView?
    - It already handles credential validation, token generation, and
      error responses (401 for invalid credentials).
    - We only need to swap in our custom serializer to add user data.

    Why AllowAny permission?
    - Login must be accessible to unauthenticated users (they're trying
      to get a token to become authenticated!).

    Request body:
        { "email": "user@example.com", "password": "securepassword" }

    Success response (200):
        {
            "access": "eyJ...",       # Short-lived access token
            "refresh": "eyJ...",      # Long-lived refresh token
            "user": {
                "id": 1,
                "name": "John Doe",
                "email": "user@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }

    Error response (401):
        { "detail": "No active account found with the given credentials" }
    """
    serializer_class = CustomTokenObtainPairSerializer

    # Override the default IsAuthenticated permission — anyone can log in
    permission_classes = (AllowAny,)
