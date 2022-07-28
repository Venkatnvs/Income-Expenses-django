from django.urls import path
from learn import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('expense-edit/<int:id>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<int:id>', views.expense_delete, name='expense-delete')
]