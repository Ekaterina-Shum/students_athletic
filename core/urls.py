from django.urls import path
from .views import lk_login, account, tournaments, events, achievements, lk_mysports, signup, logout
from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path('lk/', login_required(account), name='lk'),
    path('lk/mysports/', login_required(lk_mysports), name='lk-mysports'),

    path('lk/achievements/', login_required(achievements), name='lk-achievements'),
    path('lk/tournaments/', login_required(tournaments), name='lk-tournaments'),
    path('lk/events/', login_required(events), name='lk-events'),


    # path('clients/', clients_stock, name='clients-stock'),
    path('login/', lk_login, name='login'),
    path('signup/', signup, name='lk-signup'),
    path('logout/', logout, name='logout'),
]