from django.urls import path
from allauth import views

urlpatterns = [
    path('auth/regester', views.regester, name='regester' )
]