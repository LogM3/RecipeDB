from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['id', 'name']


admin.site.register(Tag, TagAdmin)
