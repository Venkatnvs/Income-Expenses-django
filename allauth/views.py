from django.shortcuts import render

# Create your views here.

def regester(request):
    return render(request, 'allauth/regester.html')
