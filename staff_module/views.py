from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from core.models import User, Student, StudyGroup, Sports, SportCategory
from .models import Staff, SportEvent, ParticipantsSportEvent
from django.contrib.auth.hashers import make_password

def staff_home(request):
    template = './staff_module/pages/home.html'


    staffs = Staff.objects.all()


    title = 'Личный кабинет'

    context = {
        "title": title,
        'staffs': staffs
    }

    if request.user.groups.filter(name="Преподаватели").exists():
        approved_students = Student.objects.all()
        context['approved_students'] = approved_students
    if request.user.is_superuser:
        students = Student.objects.all()

    if request.htmx:
        return render(request, './staff_module/partials/home.html', context) 
    return render(request, template, context)


def staff_create(request):
    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_staff.html'
        education_groups = StudyGroup.objects.all()
        groups = Group.objects.all()

        context = {'middle_modal': True, 'groups': groups, 'education_groups':education_groups, 'small_modal': False }
        
        return render(request, template, context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        group_system = request.POST.get('group_system')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        education_group = request.POST.get('education_group')

        group = Group.objects.get(id=group_system) 

        if email and password:
            if User.objects.filter(email=email).exists():
                return render(request, 'core/partials/signuprejected.html', context={'error_text':'Пользователь с таким email уже существует'})
            user = User.objects.create(
                email=email,
                password=make_password(password),
                is_staff=True,
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
            )
            user.groups.add(group)
            

            staff = Staff.objects.create(
                user=user
            )

            study_group = StudyGroup.objects.get(id=education_group) if education_group != 'Нет' else None
            study_group.curator = staff

            return render(request, './staff_module/partials/partial_staffs.html', context)


def events(request):
    template = './staff_module/pages/events.html'

    events = SportEvent.objects.all()

    sports = Sports.objects.all()
    type_event = SportEvent.TYPE_EVENT

    status_list = SportEvent.EVENT_STATUS
    categorys = SportCategory.objects.all()

    participants = ParticipantsSportEvent.objects.all()

    title = 'Спортивные мероприятия'

    context = {
        "title": title,
        'type_list': type_event,
        'sports': sports,
        'status_list': status_list,
        "events": events,
        'category_list': categorys,
        'participants': participants
    }

    if request.htmx:
        return render(request, './staff_module/partials/events.html', context)
    return render(request, template, context)

def filter_event(request):
    filter_sport = request.GET.get("filter_sport")
    filter_status = request.GET.get("filter_status")
    filter_type = request.GET.get("filter_type")
    filter_category = request.GET.get("filter_category")
    filter_student = request.GET.get("filter_student")
    filter_start_date = request.GET.get("start_date")
    filter_completed_date = request.GET.get("completed_date")

    events = SportEvent.objects.all()
    participants = ParticipantsSportEvent.objects.all()
    if filter_start_date:
        events = events.filter(start_event=filter_start_date)
    if filter_completed_date:
        events = events.filter(end_event=filter_completed_date)
    if filter_student:
        participant_events = ParticipantsSportEvent.objects.filter(
            Q(student__user__last_name__icontains=filter_student) |
            Q(student__user__first_name__icontains=filter_student)
        ).values_list("event_id", flat=True)
        events = events.filter(id__in=participant_events)
    if filter_sport:
        events = events.filter(sport_id=filter_sport)
    if filter_status and filter_status != "all_status":
        events = events.filter(status=filter_status)
    if filter_type and filter_type != "all_types":
        events = events.filter(type=filter_type)
    if filter_category and filter_category != "all_categorys":
        category_event= SportCategory.objects.get(id=filter_category)
        events = events.filter(category_event=category_event)

    context = {'participants':participants,
               "events": events}

    return render(request, "./staff_module/partials/events_data.html", context)

def event_create(request):
    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_event.html'

        sports = Sports.objects.all()
        type_event = SportEvent.TYPE_EVENT
        categorys = SportCategory.objects.all()

        if request.htmx:
            if 'event_sport' in request.GET:
                sport_id = request.GET.get('event_sport')
                students = Student.objects.filter(main_sport__id=sport_id)
                return render(request, './staff_module/partials/students_data.html', {'students': students})
            
        context = {'middle_modal': True, 
                   'sports': sports,
                   'categorys': categorys,
                   'type_events': type_event,
                   'small_modal': False }
        
        return render(request, template, context)

    if request.method == 'POST':
        event_sport_id = request.POST.get('event_sport')
        type_event = request.POST.get('type_event')
        event_category_id = request.POST.get('event_category')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        students = request.POST.getlist('students')

        event_sport = Sports.objects.get(id=event_sport_id) if event_sport_id != None else None
        event_category = SportCategory.objects.get(id=event_category_id)

        try:
            event = SportEvent.objects.create(
                type=type_event,
                sport=event_sport,
                category_event=event_category,
                start_event=date_start,
                end_event=date_end,
            )

            for student_id in students:
                student = Student.objects.get(user__id=student_id)
                participant = ParticipantsSportEvent.objects.create(
                    student=student,
                    event=event
                )
                participant.save()

            events = SportEvent.objects.all()
            participants = ParticipantsSportEvent.objects.all()

            return render(request, './staff_module/partials/events_data.html', {'events': events, 'participants': participants})
        except Exception as e:
            print(e)
            return render(request, './staff_module/partials/events_data.html', context)

def event_detail(request, *args, **kwargs):
    event_id = kwargs.get('event_id')
    template = './staff_module/pages/event_detail.html'

    event = get_object_or_404(SportEvent, id=event_id)

    participants = ParticipantsSportEvent.objects.filter(event=event)

    title = 'Спортивные мероприятия'

    context = {
        "title": title,
        'event': event,
        'participants': participants
    }

    if request.htmx:
        return render(request, './staff_module/partials/event_detail.html', context)
    return render(request, template, context)

def event_add_student(request, *args, **kwargs):
    event_id = kwargs.get('event_id')
    sport_id = kwargs.get('sport_id')

    sport = Sports.objects.get(id=sport_id)
    event = SportEvent.objects.get(id=event_id)

    participants = ParticipantsSportEvent.objects.filter(event=event).values_list('student_id', flat=True)

    if request.method == 'GET':
        template = './staff_module/components/modals/add/modal_add_student_event.html'

        students = Student.objects.filter(main_sport=sport).exclude(user__id__in=participants)

        if request.htmx:
            if 'event_sport' in request.GET:
                sport_id = request.GET.get('event_sport')
                students = Student.objects.filter(main_sport__id=sport_id)
                return render(request, './staff_module/partials/students_data.html', {'students': students})
            
        context = {'middle_modal': True, 
                   'sport': sport,
                   'students': students,
                   'event': event,
                   'small_modal': False }
        
        return render(request, template, context)
    
    if request.method == 'POST':
        students = request.POST.getlist('students')

        try:
            for student_id in students:
                student = Student.objects.get(user__id=student_id)
                participant = ParticipantsSportEvent.objects.create(
                    student=student,
                    event=event
                )
                participant.save()

            participants = ParticipantsSportEvent.objects.all()

            return render(request, './staff_module/partials/event_students_participants.html', {'participants': participants})
        except Exception as e:
            print(e)
            return render(request, './staff_module/partials/event_students_participants.html', {'participants': participants})

def staff_students_approved(request, *args, **kwargs):
    if request.method == 'POST':
        student_id = kwargs.get('id')

        approved_students = Student.objects.filter(approved=False, study_group__curator=request.user)

        user = User.objects.filter(id=student_id).first()
        student = Student.objects.get(user=user)
        student.approved = True
        student.save()

        context = {
            'approved_students': approved_students
        }

        return render(request, './staff_module/partials/partial_approved_students.html', context)

def users(request):
    template = './staff_module/pages/users.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }
    if request.htmx:
        return render(request, './staff_module/partials/users.html', context)  
    return render(request, template, context)
