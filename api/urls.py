from django.urls import include, path

from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_notifier, name='test_notify'),
]