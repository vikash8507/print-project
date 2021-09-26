from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'is_staff', 'is_active', 'points', )
    fieldsets = (
        (None, {'fields': ("username", 'email', 'password', "first_name", 'last_name', "points")}),
    )


admin.site.register(User, CustomUserAdmin)
