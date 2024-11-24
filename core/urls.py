from django.urls import path
from .views import lk_login, account, requests, signup, logout
from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path('lk/', login_required(account), name='lk'),
    path('lk/requests/', login_required(requests), name='lk-requests'),
    # path('lk/requests/<int:req_id>/', mailer_detail, name='lk-requests-detail'),
    # path('clients/', clients_stock, name='clients-stock'),
    path('login/', lk_login, name='login'),
    path('signup/', signup, name='lk-signup'),
    path('logout/', logout, name='logout'),
]