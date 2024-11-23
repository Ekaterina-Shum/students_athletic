from django.urls import path
from .views import staff_home

app_name = 'staff_module'

urlpatterns = [
    path('home/', staff_home, name='staff-home'),
]