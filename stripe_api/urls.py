from django.urls import path

from stripe_api import views

urlpatterns = [
    path('', views.Api.as_view(), name="stripe_api_endpoint"),
]
