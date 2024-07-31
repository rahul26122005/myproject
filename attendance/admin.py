from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from .models import Student, Myclass

# Custom Group Admin (if needed)
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)

# Unregister Group model if already registered
if Group in admin.site._registry:
    admin.site.unregister(Group)

# Optional: Unregister User model if you want to customize it
if User in admin.site._registry:
    admin.site.unregister(User)

# Register your models
admin.site.register(Student)
admin.site.register(Myclass)

# Register Group model with a custom admin if needed
admin.site.register(Group, CustomGroupAdmin)

# Optional: Register User model with custom admin if needed
# If you have custom fields or want to customize User admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(User, CustomUserAdmin)
