"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as translate

from core import models


class UserAdmin(BaseUserAdmin):
    """
    Note: temporary super user
    username:   admin@example.com
    pw:         2255
    Define the admin pages for users
    """
    #  ordering = ['username']
    list_display = ['username', 'email', 'first_name', 'last_name']
    # fieldsets is overwritten from base class
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (translate("Personal info"), {"fields": ("first_name",
                                                 "last_name",
                                                 "email")}),
        (
            translate("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (translate("Important dates"), {"fields": ("date_created", )}),
        # TODO  (translate('Groups'), {"fields": ("databases",)})
    )
    readonly_fields = ['date_created']
    # Fieldsets for adding a user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                            "username",
                            "password1",
                            "password2",
                            'is_active',
                            'is_staff',
                            'is_superuser',
                            ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Project)
admin.site.register(models.Database)
admin.site.register(models.BusinessClient)
