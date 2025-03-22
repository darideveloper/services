from django.contrib import admin
from socials import models


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "posted",
        "created_at",
        "updated_at",
    )
    list_filter = ("posted", "created_at", "updated_at")
    search_fields = ("title", "description", "tags", "context"),
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                    "context",
                    "tags",
                    "video_drive_url",
                    "posted",
                    "workflow_link",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    ordering = ("-id",)
