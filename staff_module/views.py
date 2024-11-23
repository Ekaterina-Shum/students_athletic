from django.shortcuts import render

def staff_home(request):
    template = './staff_module/pages/home.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)


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


def staff_students(request):
    template = './staff_module/pages/events.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)