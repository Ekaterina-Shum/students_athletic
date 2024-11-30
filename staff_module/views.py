from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import Group
from core.models import User, Student, StudyGroup
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

    if request.user.groups.filter(name="Кураторы").exists():
        approved_students = Student.objects.filter(approved=False, study_group__curator=request.user)
        context['approved_students'] = approved_students
    if request.user.is_superuser:
        students = Student.objects.all()
        
    elif request.user.groups.filter(name="Кураторы").exists():
        students = Student.objects.filter(study_group__curator=request.user)
    context['students'] = students

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


def staff_requests(request):
    template = './staff_module/pages/requests.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)


def staff_events(request):
    template = './staff_module/pages/events.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)


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

def staff_students(request):
    template = './staff_module/pages/events.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)




def event_create(request):
    if request.method == 'GET':
        template = './staff_module/components/modals/create/modal_create_event.html'
        education_groups = StudyGroup.objects.all()
        groups = Group.objects.all()

        context = {'middle_modal': True, 'groups': groups, 'education_groups':education_groups, 'small_modal': False }
        
        return render(request, template, context)

    if request.method == 'POST':
        email = request.POST.get('email')

        return render(request, './staff_module/partials/partial_staffs.html', context)
