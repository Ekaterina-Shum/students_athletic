from django.urls import path
from .views import staff_home, staff_requests, staff_events, staff_create, staff_students, staff_students_approved
from django.contrib.auth.decorators import login_required

app_name = 'staff_module'

urlpatterns = [
    path('home/', login_required(staff_home), name='staff-home'),
    path('create/staff/', login_required(staff_create), name='create-staff'),

    path('requests/', login_required(staff_requests), name='staff-requests'),

    path('tournaments/', login_required(staff_events), name='staff-tournaments'),
    path('students/', login_required(staff_students), name='staff-students'),

    path('students/approved/<int:id>/', login_required(staff_students_approved), name='staff-students-approved'),
]