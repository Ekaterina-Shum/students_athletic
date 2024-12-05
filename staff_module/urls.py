from django.urls import path
from .views import staff_home, events, staff_create, users, staff_students_approved
from django.contrib.auth.decorators import login_required

app_name = 'staff_module'

urlpatterns = [
    path('home/', login_required(staff_home), name='staff-home'),
    path('create/staff/', login_required(staff_create), name='create-staff'),

    path('events/', login_required(events), name='events'),
    path('users/', login_required(users), name='staff-users'),

    path('students/approved/<int:id>/', login_required(staff_students_approved), name='staff-students-approved'),
]