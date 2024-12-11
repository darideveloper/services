from ai import views
from django.urls import path

urlpatterns = [
    path('isolated/', views.Index.as_view(), name="ai_isolated_response"),
]