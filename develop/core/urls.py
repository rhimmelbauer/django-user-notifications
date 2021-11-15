from django.urls import path

from core import views

urlpatterns = [
    path("", views.NotificationIndexView.as_view(), name="notification-index"),
]
