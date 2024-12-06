from django.urls import path
from .views import staff_home, events, system_data, system_education_group, student_create, system_specialization, system_sports, event_add_student, students, event_complete, staff_create, event_detail_save_achievement, event_create, users, event_detail, staff_students_approved, filter_event
from django.contrib.auth.decorators import login_required

app_name = 'staff_module'

urlpatterns = [
    path('home/', login_required(staff_home), name='staff-home'),
    path('system-data/', login_required(system_data), name='system-data'),
    path('create/staff/', login_required(staff_create), name='create-staff'),
    path('create/student/', login_required(student_create), name='create-student'),
    
    path('system/create/sport/', login_required(system_sports), name='system-create-sport'),
    path('system/create/specialization/', login_required(system_specialization), name='system-create-specialization'),
    path('system/create/education-group/', login_required(system_education_group), name='system-create-education-group'),

    path('events/', login_required(events), name='events'),
    path('events/filters/', login_required(filter_event), name='events-filters'),
    path('events/create/', login_required(event_create), name='event-create'),
    path('events/<int:event_id>/', login_required(event_detail), name='event-detail'),
    path('events/<int:event_id>/complete/', login_required(event_complete), name='event-detail-complete'),
    path('events/<int:event_id>/student/<int:student_id>/save/achievement/', login_required(event_detail_save_achievement), name='event-detail-save-achievement'),
    path('events/<int:event_id>/<int:sport_id>/add/student/', login_required(event_add_student), name='event-detail-add-student'),
    path('users/', login_required(users), name='staff-users'),
    path('students/', login_required(students), name='staff-students'),

    path('students/approved/<int:id>/', login_required(staff_students_approved), name='staff-students-approved'),
]