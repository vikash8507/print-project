from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'name', 'is_active', 'points', 'phone', )
    fieldsets = (
        (None, {'fields': ("username", 'email', 'password', "name", 'phone', "points", "shop_name", "shop_address")}),
    )


admin.site.register(User, CustomUserAdmin)
