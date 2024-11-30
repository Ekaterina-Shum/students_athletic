from django.urls import path
from .views import lk_login, account, requests, create_request, lk_mysports, signup, logout
from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path('lk/', login_required(account), name='lk'),
    path('lk/requests/', login_required(requests), name='lk-requests'),
    path('lk/create/request/', login_required(create_request), name='lk-create-request'),
    path('lk/mysports/', login_required(lk_mysports), name='lk-mysports'),
    # path('lk/requests/<int:req_id>/', mailer_detail, name='lk-requests-detail'),
    # path('clients/', clients_stock, name='clients-stock'),
    path('login/', lk_login, name='login'),
    path('signup/', signup, name='lk-signup'),
    path('logout/', logout, name='logout'),
]