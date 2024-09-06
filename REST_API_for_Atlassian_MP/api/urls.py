from django.urls import path
from . import views

urlpatterns = [
    path('get-apps/', views.get_apps)
]