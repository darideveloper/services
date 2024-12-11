from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from contactform import urls as contactform_urls
from ai import urls as ai_urls


urlpatterns = [
    path('', core_views.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('contact-form/', include(contactform_urls)),
    path('stripe-api/', include('stripe_api.urls')),
    path('ai/', include(ai_urls)),
]
