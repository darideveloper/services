from django.contrib import admin
from socials import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "video_drive_name",
        "posted",
        "created_at",
        "updated_at",
    )
    list_filter = ("posted", "created_at", "updated_at")
    search_fields = ("video_drive_name", "description", "tags", "context"),
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-id",)
