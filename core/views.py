from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.http import JsonResponse
from .models import User, Student
from django.contrib.auth.hashers import make_password
import json


def logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        approved_password = request.POST.get('approved_password')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')

        if password != approved_password:
            return HttpResponse('Пароли не совпадают', status=400)

        if User.objects.filter(email=email).exists():
            return HttpResponse('Пользователь с таким email уже существует', status=400)
        
        user = User.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic
        )

        Student.objects.create(
            user=user,
            approved=False,
        )

        return HttpResponse('Регистрация прошла успешно!', status=200)

    return render(request, 'core/pages/registration.html')

def login(request):
    template = './core/pages/login.html'
    if request.user.is_authenticated:
        return redirect('core:lk')
    
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active == True:
                login(request, user)
            else:
                return JsonResponse({'error': 'Ошибка'}, status=302)
            return redirect('core:login')

        else:

            messages.error(request, f'Неверные данные. Пожалуйста, повторите попытку')
            return redirect('core:login')

    else:
        return render(request, template)



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


