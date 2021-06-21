from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

from .views import (register, UsernameValidationView, EmailValidationView, profile2,
					login, user_profile, BankView, withdrawl)




urlpatterns=[


    path('register/',views.register, name="register"),
    path('validate-username/',csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/',csrf_exempt(EmailValidationView.as_view()), name='validate-email'),

    path('profile/', views.profile2, name='profile'),
    path('dashboard/', views.user_profile, name='user_profile'),

    path('login/', views.loginpage, name="login"),

    path('peerwork/wallet/', BankView.as_view(), name='wallet'),
    # path('peerwork/wallet/', BankUpdateView.as_view(), name='wallet-update'),
    path('withdraw/money/<slug:slug>', views.withdrawl, name='withdraw'),

]