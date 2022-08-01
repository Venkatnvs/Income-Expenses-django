from django.shortcuts import render
from learn.models import Expense
from userincome.models import UserIncome
from django.http import JsonResponse
import datetime

# Create your views here.
def LastMonthData(request):
    today_date = datetime.date.today()
    last_months_ago =today_date - datetime.timedelta(days=30)
    expenses = Expense.objects.filter(owner=request.user, date__gte=last_months_ago, date__lte=today_date)
    income = UserIncome.objects.filter(owner=request.user, date__gte=last_months_ago, date__lte=today_date)
    finalresult1= {}
    finalresult2= {}

    def get_category(expenses):
        return expenses.category
    def get_source(income):
        return income.source

    category_list = list(set(map(get_category, expenses)))
    source_list = list(set(map(get_source, income)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount
    def get_income_source_amount(source):
        amount = 0
        filter_by_source = income.filter(source=source)
        for item in filter_by_source:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalresult1[y]=get_expense_category_amount(y)
    for x in income:
        for y in source_list:
            finalresult2[y]=get_income_source_amount(y)

    return JsonResponse({'expense_category_amount':finalresult1, 'income_source_amount':finalresult2}, safe=False)


def LastMonth(request):
    return render(request, 'dashboard/index.html')