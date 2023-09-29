from django.contrib import admin
from contactform import models

# Contact forms models
@admin.register(models.User)
class ContactFormUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'to_email')
    ordering = ['name']

@admin.register(models.History)
class ContactFormHistoryAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'user', 'subject', 'sent')
    ordering = ['datetime', 'sent']

@admin.register(models.BlackList)
class ContactFormBlackListAdmin(admin.ModelAdmin):
    list_display = ('to_email',)
    ordering = ['to_email']
