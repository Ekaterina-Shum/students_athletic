from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from core.models import User, Student, StudyGroup, Sports, SportCategory, SportAchievement, Specialization
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


def system_data(request):
    template = './staff_module/pages/system_data.html'

    sports = Sports.objects.all()
    study_groups = StudyGroup.objects.all()
    specializations = Specialization.objects.all()
    staffs = Staff.objects.all()


    title = 'Управление данными системы'

    context = {
        "title": title,
        'sports': sports,
        'specializations': specializations,
        'education_groups': study_groups,
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


def system_sports(request):
    sports = Sports.objects.all()
    specializations = Specialization.objects.all()
    education_groups = StudyGroup.objects.all()

    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_sport.html'
        education_groups = StudyGroup.objects.all()

        context = {'middle_modal': True, 'small_modal': True }
        
        return render(request, template, context)

    if request.method == 'POST':
        sport_name = request.POST.get('sport_name')


        if sport_name:
            Sports.objects.create(
                name=sport_name,
            )

            context = {'sports': sports, 'specializations': specializations, 'education_groups': education_groups}

            return render(request, './staff_module/partials/system_data.html', context)


def system_specialization(request):
    sports = Sports.objects.all()
    specializations = Specialization.objects.all()
    education_groups = StudyGroup.objects.all()

    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_specialization.html'
        education_groups = StudyGroup.objects.all()

        context = {'middle_modal': True, 'small_modal': True }
        
        return render(request, template, context)

    if request.method == 'POST':
        specialization_name = request.POST.get('specialization_name')
        specialization_code = request.POST.get('specialization_code')


        if specialization_name and specialization_code:
            Specialization.objects.create(
                name=specialization_name,
                code=specialization_code
            )

            context = {'sports': sports, 
                       'education_groups': education_groups,
                       'specializations': specializations}

            return render(request, './staff_module/partials/system_data.html', context)


def system_education_group(request):
    sports = Sports.objects.all()
    specializations = Specialization.objects.all()
    education_groups = StudyGroup.objects.all()

    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_study_group.html'
        education_groups = StudyGroup.objects.all()
        level_education = StudyGroup.LEVEL_EDUCATION

        context = {'middle_modal': True, 
                   'specializations': specializations, 
                   'levels_education':level_education, 'education_groups':education_groups, 'small_modal': False }
        
        return render(request, template, context)

    if request.method == 'POST':
        name_group = request.POST.get('name_group')
        specialization_id = request.POST.get('specialization_id')
        level_education = request.POST.get('level_education')
        group_term = request.POST.get('group_term')
        group_course = request.POST.get('group_course')

        specialization = Specialization.objects.get(id=specialization_id)

        if specialization_id and name_group:
            StudyGroup.objects.create(
                name=name_group,
                course=group_course,
                specialization=specialization,
                term=group_term,
                level_education=level_education
            )

            context = {'sports': sports, 
                       'education_groups': education_groups,
                       'specializations': specializations}

            return render(request, './staff_module/partials/system_data.html', context)


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


def student_create(request):
    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_student.html'
        education_groups = StudyGroup.objects.all()

        context = {'middle_modal': True, 'education_groups':education_groups, 'small_modal': False }
        
        return render(request, template, context)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        education_group_id = request.POST.get('education_group')

        group = Group.objects.get(name='Студенты') 
        study_group = StudyGroup.objects.get(id=education_group_id)

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
            

            Student.objects.create(
                user=user,
                approved=True,
                study_group=study_group
            )

            students = Student.objects.all()

            return render(request, './staff_module/pages/students.html', {"students": students})



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

def event_complete(request, *args, **kwargs):
    event_id = kwargs.get('event_id')
    template = './staff_module/partials/event_detail.html'

    event = get_object_or_404(SportEvent, id=event_id)
    participants = ParticipantsSportEvent.objects.filter(event=event)
    event_result = ParticipantsSportEvent.RESULT_CHOICES
    event_position = ParticipantsSportEvent.POSITION_CHOICES
    if request.method == 'GET':
        event.status = 'completed'
        event.save()
        
        title = 'Спортивное мероприятие'

        context = {
            "title": title,
            'event': event,
            'event_result': event_result,
            'event_position': event_position,
            'participants': participants
        }

        return render(request, template, context)

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

    event_result = ParticipantsSportEvent.RESULT_CHOICES
    event_position = ParticipantsSportEvent.POSITION_CHOICES
    if request.method == 'GET':
        title = 'Спортивное мероприятие'

        context = {
            "title": title,
            'event': event,
            'event_result': event_result,
            'event_position': event_position,
            'participants': participants
        }

        if request.htmx:
            return render(request, './staff_module/partials/event_detail.html', context)
        return render(request, template, context)


def event_detail_save_achievement(request, *args, **kwargs):
    event_id = kwargs.get('event_id')
    student_id = kwargs.get('student_id')
    mvp_status = kwargs.get('mvp_status')

    mvp = False

    if mvp_status == 'mvp_true':
        mvp = True

    event = get_object_or_404(SportEvent, id=event_id)

    student = Student.objects.get(user__id=student_id)
    participant = ParticipantsSportEvent.objects.get(event=event)
    

    if request.method == 'POST':
        event_position = request.POST.get('event_position')
        event_result = request.POST.get('event_result')

        try:
            achievement = SportAchievement.objects.create(
                student = student,
                sport=event.sport,
                event=event,
                position=event_position
            )
            achievement.save()

            participant.result=event_result
            participant.position=event_position
            participant.mvp=mvp
            participant.save()


            participants = ParticipantsSportEvent.objects.filter(event=event)

            return render(request, './staff_module/partials/event_students_participants.html', {'participants': participants})
        except Exception as e:
            print(e)
            return render(request, './staff_module/partials/event_students_participants.html', {'participants': participants})


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


def students(request):
    template = './staff_module/pages/students.html'

    title = 'Студенты'

    students = Student.objects.all()

    context = {
        "title": title,
        "students": students
    }
    if request.htmx:
        return render(request, './staff_module/partials/students.html', context)  
    return render(request, template, context)