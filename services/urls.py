from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from contactform import urls as contactform_urls
from ai import urls as ai_urls
from core.views import LoginView, ProfileView


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Redirects
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('auth/', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    
    # Apps
    path('contact-form/', include(contactform_urls)),
    path('stripe-api/', include('stripe_api.urls')),
    path('ai/', include(ai_urls)),
    path('activity-watch/', include('activitywatch.urls')),
    
    # auth endpoint
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
]
