from django.urls import path
from .views import staff_home, staff_requests, staff_events, staff_students

app_name = 'staff_module'

urlpatterns = [
    path('home/', staff_home, name='staff-home'),
    path('requests/', staff_requests, name='staff-requests'),
    path('events/', staff_events, name='staff-events'),
    path('students/', staff_students, name='staff-students'),
]