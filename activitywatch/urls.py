from django.urls import path
from . import views

app_name = 'activitywatch'

urlpatterns = [
    path('logs/<str:origin_key>/', views.ActivityWatchView.as_view(), name='activity-watch'),
]
