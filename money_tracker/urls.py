from django.urls import path
from . import views

app_name = 'money_tracker'

urlpatterns = [
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/add_category/', views.add_category, name='add_category'),
    path('expenses/chart/', views.expense_chart, name='expense_chart'),
]