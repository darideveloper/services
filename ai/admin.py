from django.contrib import admin
from ai import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'prompt')
    ordering = ['name']
    search_fields = ['name', 'prompt']