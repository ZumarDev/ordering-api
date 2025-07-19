from django.contrib import admin
from .models import User

from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "role",
                    "is_staff",
                    "is_superuser",
                    "password",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser")}),
    )
    list_display = ("id", "full_name", "phone_number", "role")
    list_filter = ("role",)
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("first_name",)

    def full_name(self, obj):
        return f"{obj.first_name.title()} {obj.last_name.title()}"

    full_name.short_description = "Full Name"


admin.site.register(User, CustomUserAdmin)
