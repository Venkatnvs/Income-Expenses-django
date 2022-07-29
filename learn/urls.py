from django.urls import path
from learn import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('expense-edit/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses')
]