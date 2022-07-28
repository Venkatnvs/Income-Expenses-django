from django.shortcuts import render
import os
import json
from django.conf import settings
from django.contrib import messages
from .models import Userprefer

# Create your views here.

def index(request):
    user_prefer = None
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k,v in data.items():
            currency_data.append({'name':k, 'value':v})

    check = Userprefer.objects.filter(user=request.user).exists()
    if check:
        user_prefer = Userprefer.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'userprefer/index.html', {'currencies':currency_data, 'user_prefer':user_prefer})
        
    elif request.method == 'POST':
        currency = request.POST['currency']
        if check:
            user_prefer.currency=currency
            user_prefer.save()
        else:
            Userprefer.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes Saved')
        return render(request, 'userprefer/index.html', {'currencies':currency_data, 'user_prefer':user_prefer})
