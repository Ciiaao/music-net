from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, AppUser

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Custom Profile Data'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

# Register the Proxy model with our custom layout attached
admin.site.register(AppUser, CustomUserAdmin)