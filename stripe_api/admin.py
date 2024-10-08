from django.contrib import admin
from stripe_api.models import Credentilas


@admin.register(Credentilas)
class CredentilasAdmin(admin.ModelAdmin):
    
    list_display = ('username', 'public_key')
    search_fields = ('username', 'public_key', 'secret_key')
    list_filter = ('created', 'last_updated')
    ordering = ['username']
