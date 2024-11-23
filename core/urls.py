from django.urls import path
from .views import login, account, requests, signup

app_name = 'core'

urlpatterns = [
    path('lk/', account, name='lk'),
    path('lk/requests/', requests, name='lk-requests'),
    # path('lk/requests/<int:req_id>/', mailer_detail, name='lk-requests-detail'),
    # path('clients/', clients_stock, name='clients-stock'),
    path('login/', login, name='login'),
    path('signup/', signup, name='lk-signup'),
]