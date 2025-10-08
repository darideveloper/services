from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

import boto3

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
    list_display = ("credentials", "file_link", "created_at")
    list_filter = ("credentials", "created_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    def file_link(self, obj):
        if not obj.backup_file:
            return "No file"
        
        print(f"Django file name: {obj.backup_file.name}")
        
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )
        
        # List what's actually in S3
        try:
            response = s3.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Prefix='private/backups',
                MaxKeys=10
            )
            print("\n=== Files in private/backups ===")
            for item in response.get('Contents', []):
                print(f"  {item['Key']}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Try with private prefix
        s3_key = obj.backup_file.name
        if not s3_key.startswith('private/'):
            s3_key = f"private/{s3_key}"
        
        print(f"Trying key: {s3_key}")
        
        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": s3_key,
            },
            ExpiresIn=3600,
        )
        
        return format_html(
            '<a class="btn btn-primary" href="{}" target="_blank">Download</a>', url
        )

    file_link.allow_tags = True
    file_link.short_description = "Download"

    file_link.allow_tags = True
    file_link.short_description = "Download"
