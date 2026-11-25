"""
accounts/admin.py — Admin Configuration for Custom User Model

Registers our CustomUser model with Django's admin interface so we can:
- View, search, and filter users through the web-based admin panel.
- Create and edit user accounts manually during development.

Why customize UserAdmin?
- Django's default UserAdmin expects fields like 'username' and 'first_name'
  which don't exist in our CustomUser model (we use 'email' and 'name').
- Without customization, the admin panel would crash or show wrong fields.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the CustomUser model.

    Overrides:
    - list_display: Columns shown in the user list view.
    - list_filter: Sidebar filters for quick filtering.
    - search_fields: Fields searchable from the admin search bar.
    - ordering: Default sort order for the user list.
    - fieldsets: Field groupings shown when viewing/editing an existing user.
    - add_fieldsets: Field groupings shown when creating a new user.
    """

    # Columns visible in the admin user list page
    list_display = ('email', 'name', 'is_staff', 'is_active', 'created_at')

    # Sidebar filters for narrowing down the user list
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    # Fields that the admin search bar queries against
    search_fields = ('email', 'name')

    # Default ordering: newest users first
    ordering = ('-created_at',)

    # --- Fieldsets for EDITING an existing user ---
    # Grouped into logical sections for better readability
    fieldsets = (
        # Main section: core identity fields
        (None, {'fields': ('email', 'password')}),

        # Personal info section
        ('Personal Info', {'fields': ('name',)}),

        # Permissions section: control access levels
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )

    # --- Fieldsets for CREATING a new user ---
    # Shown when clicking "Add User" in admin
    # Uses wide CSS class for better form layout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2',
                       'is_staff', 'is_active'),
        }),
    )


# Register our CustomUser model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)
