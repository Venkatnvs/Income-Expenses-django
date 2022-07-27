from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('regester', Registration.as_view(), name='register' ),
    path('login', Registration.as_view(), name='login' ),
    path('validate-username', csrf_exempt(UsernameValidation.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name='validate-email'),
    path('activate-user/<uidb64>/<token>', Verification.as_view(), name='activate')
]