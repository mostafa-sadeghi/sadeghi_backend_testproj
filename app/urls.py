from django.urls import path
from .views import home_view

urlpatterns = [
    path('dashboard/', home_view),
]


