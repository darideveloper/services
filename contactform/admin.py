from django.contrib import admin
from contactform import models


@admin.register(models.User)
class ContactFormUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'to_email')
    ordering = ['name']


@admin.register(models.History)
class ContactFormHistoryAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'user', 'subject', 'sent')
    ordering = ['datetime', 'sent']
    list_filter = ['user', 'sent']


@admin.register(models.EmailSender)
class ContactFormEmailSenderAdmin (admin.ModelAdmin):
    list_display = ('host', 'port', 'username', 'use_ssl')
    ordering = ['host', 'port']
