from django.shortcuts import render

def staff_home(request):
    template = './staff_module/pages/home.html'

    title = 'Личный кабинет'

    context = {
        "title": title
    }

    return render(request, template, context)

