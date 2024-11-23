from django.urls import path
from .views import staff_home, staff_requests, staff_events, staff_create, staff_students
from django.contrib.auth.decorators import login_required

app_name = 'staff_module'

urlpatterns = [
    path('home/', login_required(staff_home), name='staff-home'),
    path('create/staff/', login_required(staff_create), name='create-staff'),
    path('requests/', login_required(staff_requests), name='staff-requests'),
    path('events/', login_required(staff_events), name='staff-events'),
    path('students/', login_required(staff_students), name='staff-students'),
]