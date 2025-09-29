from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from contactform import urls as contactform_urls
# from ai import urls as ai_urls
from core.views import LoginView, ProfileView

from rest_framework import routers
from blog import views as blog_views


router = routers.DefaultRouter()

# Blog endpoints
router.register(
    r'posts',
    blog_views.PostViewSet,
    basename='posts'
)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Redirects
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('auth/', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    
    # Apps
    path('contact-form/', include(contactform_urls)),
    path('stripe-api/', include('stripe_api.urls')),
    # path('ai/', include(ai_urls)),
    # path('activity-watch/', include('activitywatch.urls')),
    
    # auth endpoint
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    
    # API URLs
    path('api/', include(router.urls)),
]

if not settings.STORAGE_AWS:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
