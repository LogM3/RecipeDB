from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)
