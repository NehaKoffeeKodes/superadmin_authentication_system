from django.contrib import admin
from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_superuser', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('totp_secret', 'is_verify', 'is_default_change')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
    )

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = "Full Name"


