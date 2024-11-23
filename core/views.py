from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .models import User, Student, StudyGroup
from django.urls import reverse
from staff_module.models import Staff
from django.contrib.auth.hashers import make_password


def logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('core:lk')
        education_groups = StudyGroup.objects.all()

        context = {'education_groups': education_groups}

        return render(request, 'core/pages/registration.html', context)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        approved_password = request.POST.get('approved_password')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        education_group = request.POST.get('education_group')

        if password != approved_password:
            return render(request, 'core/partials/signuprejected.html', context={'error_text':'Пароли не совпадают'})

        if User.objects.filter(email=email).exists():
            return render(request, 'core/partials/signuprejected.html', context={'error_text':'Пользователь с таким email уже существует'})
        
        
        study_group = StudyGroup.objects.get(id=education_group)

        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )

        Student.objects.create(
            user=user,
            study_group=study_group
        )


        return render(request, 'core/partials/signupgone.html')

def lk_login(request):
    template = './core/pages/login.html'

    if request.user.is_authenticated:
        return JsonResponse({'redirect_url': reverse('core:lk')}, status=200)

    if request.method == "POST":
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            return render(request, 'core/partials/loginerror.html', context={'error_text': 'Пожалуйста, заполните все поля'}, status=400)

        user = authenticate(email=email, password=password)

        if user is not None:
            student = Student.objects.filter(user=user).first()
            if student:
                if student.approved:
                    login(request, user)
                    return JsonResponse({'redirect_url': reverse('core:lk')}, status=200)
                else:
                    return render(request, 'core/partials/loginerror.html', context={
                        'error_text': 'Ваш профиль еще не подтвержден куратором.'
                    }, status=400)

            if user.is_superuser:
                login(request, user)
                return JsonResponse({'redirect_url': reverse('staff_module:staff-home')}, status=200)

            staff = Staff.objects.filter(user=user).first()
            if staff and user.is_active:
                if user.is_staff:
                    curator_group = Group.objects.filter(name='Кураторы').first()
                    if curator_group and curator_group in user.groups.all():
                        login(request, user)
                        return JsonResponse({'redirect_url': reverse('staff_module:staff-home')}, status=200)

                return render(request, 'core/partials/loginerror.html', context={
                    'error_text': 'Доступ запрещен.'
                })

        return render(request, 'core/partials/loginerror.html', context={
            'error_text': 'Некорректные учетные данные.'
        })

    return render(request, template)

def logout(request):
    auth_logout(request)

    return redirect('core:login')


def account(request):
    template = './core/pages/account.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)


def requests(request):
    template = './core/pages/requests.html'

    title = 'Запросы'

    context = {
        "title": title
    }

    return render(request, template, context)


