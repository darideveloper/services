from django.contrib import admin
from django.urls import path, include
from contactform import urls as contactform_urls
from core import views as core_views


urlpatterns = [
    path('', core_views.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('contact-form/', include(contactform_urls)),
]
