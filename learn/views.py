from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from userprefer.models import Userprefer

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            decription__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)



@login_required
def home(request):
    #categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator= Paginator(expenses, 5)
    page_no = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_no)
    currency = Userprefer.objects.get(user=request.user).currency
    context = {
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request, 'learn/main.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context= {
        'categories':categories,
        'values':request.POST
        }
    if request.method == 'GET':
        return render(request, 'learn/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'learn/add_expense.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'learn/add_expense.html', context)
        if category == 'Choose...':
            messages.error(request, 'Category is required')
            return render(request, 'learn/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'learn/add_expense.html', context)
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, decription=decription)
        messages.success(request, 'Expense saved successfully')
        return redirect('home')



def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories
        }
    if request.method == 'GET':
        return render(request, 'learn/expense-edit.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        decription = request.POST['decription']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'learn/expense-edit.html', context)
        if not decription:
            messages.error(request, 'Decription is required')
            return render(request, 'learn/expense-edit.html', context)
        if category == 'Choose...':
            messages.error(request, 'Category is required')
            return render(request, 'learn/expense-edit.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'learn/expense-edit.html', context)

        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.decription=decription
        expense.save()

        messages.success(request, 'Expense Updated successfully')
        return redirect('home')


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense is removed')
    return redirect('home')

