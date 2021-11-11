from django.urls import path

from core import views

urlpatterns = [
    path("", views.ReminderIndexView.as_view(), name="reminder-index"),
]
