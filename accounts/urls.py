"""
accounts/urls.py — Authentication URL Routes

Maps URL paths to views for user authentication:
- /api/auth/register/      → Create a new user account
- /api/auth/login/         → Authenticate and receive JWT tokens
- /api/auth/token/refresh/ → Get a new access token using a refresh token

Why separate urls.py per app?
- Keeps URL definitions modular and organized.
- Each app owns its routes — easy to find, test, and modify.
- The root urls.py includes these via include('accounts.urls').
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView

urlpatterns = [
    # Register a new user
    # POST /api/auth/register/
    # Body: { "name": "...", "email": "...", "password": "...", "password2": "..." }
    # Returns: 201 with user data on success
    # Permissions: AllowAny (no authentication required)
    path('register/', RegisterView.as_view(), name='auth-register'),

    # Log in and receive JWT tokens
    # POST /api/auth/login/
    # Body: { "email": "...", "password": "..." }
    # Returns: 200 with access token, refresh token, and user data
    # Permissions: AllowAny (no authentication required)
    path('login/', LoginView.as_view(), name='auth-login'),

    # Refresh an expired access token
    # POST /api/auth/token/refresh/
    # Body: { "refresh": "<refresh_token>" }
    # Returns: 200 with a new access token
    # Why: Access tokens expire in 60 minutes. Instead of forcing users
    # to re-enter credentials, the frontend sends the refresh token to
    # get a new access token silently.
    # Permissions: AllowAny (uses the refresh token itself for validation)
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
