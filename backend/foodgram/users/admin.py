from django.contrib import admin

from .models import User, UserFollow


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']
    search_fields = ['id', 'username', 'email']


admin.site.register(User, UserAdmin)
admin.site.register(UserFollow)
