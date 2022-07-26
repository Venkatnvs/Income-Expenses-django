from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.

class Registration(View):
    def get(self, request):
        return render(request, 'allauth/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'FieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password)<8:
                    messages.error(request, 'Password too short')
                    return render(request, 'allauth/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()


                email_subject = 'Activate your account'
                email_body = 'test'

                email = EmailMessage(
                    email_subject,
                    email_body,
                    '202305442mar.venkatswaroope3@gmail.com',
                    [email],
                )
                email.send(fail_silently=False)


                messages.success(request, 'Account successfully created')
                return render(request, 'allauth/register.html')


        return render(request, 'allauth/register.html')



class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Usernmae should only contain alphanumeric characters'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry usernmae is already taken'})
        return JsonResponse({'username_valid':True})


class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry email is already registered'})
        return JsonResponse({'email_valid':True})

class Verification(View):
    def get(self, request, uidb64, token):
        return redirect('login')