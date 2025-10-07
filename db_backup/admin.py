from django.contrib import admin

from db_backup import models


@admin.register(models.Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    list_display = ("project", "username", "host", "port", "database", "enabled")
    search_fields = ("project", "username", "host", "port", "database")
    list_filter = ("username", "host", "database")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(models.Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ("credentials", "backup_file", "created_at")
    list_filter = ("credentials", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
