from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userprefer.models import Userprefer
from django.contrib import messages
from django.http import JsonResponse
import json


# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            decription__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)

        data = income.values()
        return JsonResponse(list(data), safe=False)



@login_required
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    paginator= Paginator(income, 5)
    page_no = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_no)
    currency = Userprefer.objects.get(user=request.user).currency
    context = {
        'income':income,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'userincome/index.html', context)

def add_income(request):
    source = Source.objects.all()
    context= {
        'sources':source,
        'values':request.POST
        }
    if request.method == 'GET':
        return render(request, 'userincome/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/add_income.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userincome/add_income.html', context)
        if source== 'Choose...':
            messages.error(request, 'Source is required')
            return render(request, 'userincome/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/add_income.html', context)
        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, decription=decription)
        messages.success(request, 'Income saved successfully')
        return redirect('income')

def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income':income,
        'values':income,
        'source':sources
        }
    if request.method == 'GET':
        return render(request, 'userincome/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'userincome/edit_income.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'userincome/edit_income.html', context)
        if source == 'Choose...':
            messages.error(request, 'Source is required')
            return render(request, 'userincome/edit_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'userincome/edit_income.html', context)

        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.decription=decription
        income.save()

        messages.success(request, 'Income Updated successfully')
        return redirect('income')


def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income is removed')
    return redirect('income')

