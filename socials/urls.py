from django.urls import path

from socials import views


urlpatterns = [
    path('video/', views.VideoView.as_view()),
]
