"""
accounts/models.py — Custom User Model

Why a custom user model?
- Django's default User model uses 'username' as the login identifier.
- For a healthcare API, email-based login is more practical and professional.
- Django docs strongly recommend setting AUTH_USER_MODEL BEFORE the first
  migration, because changing it later is extremely difficult.

We extend AbstractBaseUser + PermissionsMixin for full control over fields
and authentication behavior, while keeping Django's permission system intact.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser.

    Why: AbstractBaseUser requires a custom manager that defines
    create_user() and create_superuser() methods, because the default
    UserManager expects a 'username' field which we've removed.
    """

    def create_user(self, email, name, password=None, **extra_fields):
        """
        Create and return a regular user with an email, name, and password.
        - Normalizes email (lowercases the domain part) to prevent duplicates
          like User@Gmail.com vs user@gmail.com.
        - Hashes the password using Django's built-in hashers (PBKDF2 by default).
        """
        if not email:
            raise ValueError('The Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # Hashes the raw password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Create and return a superuser (admin) with elevated permissions.
        - Sets is_staff=True so the user can access Django admin.
        - Sets is_superuser=True so the user has all permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email instead of username for authentication.

    Fields:
        email: Unique email address — used as the login identifier (USERNAME_FIELD).
        name: Full name of the user.
        is_active: Soft-delete flag — inactive users cannot authenticate.
        is_staff: Required by Django admin — allows access to admin panel.
        created_at: Timestamp of when the account was created.
    """
    email = models.EmailField(
        unique=True,
        max_length=255,
        help_text='Unique email address used for authentication'
    )
    name = models.CharField(
        max_length=255,
        help_text='Full name of the user'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user account is active'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can access the admin site'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the user account was created'
    )

    # Tell Django to use our custom manager
    objects = CustomUserManager()

    # Use email as the unique identifier for authentication (instead of username)
    USERNAME_FIELD = 'email'

    # Fields prompted for when creating a superuser via `createsuperuser` command
    # (email is already required by USERNAME_FIELD, so only name is listed here)
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
