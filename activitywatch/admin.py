from django.contrib import admin
from activitywatch import models


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("origin", "created_at")
    list_filter = ("origin",)
    search_fields = ("origin",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
