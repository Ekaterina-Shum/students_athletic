from django.urls import path
from .views import staff_home, events, event_add_student, staff_create, event_create, users, event_detail, staff_students_approved, filter_event
from django.contrib.auth.decorators import login_required

app_name = 'staff_module'

urlpatterns = [
    path('home/', login_required(staff_home), name='staff-home'),
    path('create/staff/', login_required(staff_create), name='create-staff'),

    path('events/', login_required(events), name='events'),
    path('events/filters/', login_required(filter_event), name='events-filters'),
    path('events/create/', login_required(event_create), name='event-create'),
    path('events/<int:event_id>/', login_required(event_detail), name='event-detail'),
    path('events/<int:event_id>/<int:sport_id>/add/student/', login_required(event_add_student), name='event-detail-add-student'),
    path('users/', login_required(users), name='staff-users'),

    path('students/approved/<int:id>/', login_required(staff_students_approved), name='staff-students-approved'),
]