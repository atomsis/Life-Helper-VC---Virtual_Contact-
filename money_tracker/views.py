from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

import json


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    # expenses = Expense.objects.all()

    return render(request, 'money_tracker/expense_list.html', {'expenses': expenses, 'section': 'expense_list'})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST,user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('money_tracker:expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'money_tracker/add_expense.html', {'form': form})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST,user=request.user)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Category.objects.filter(user=request.user, name=name).exists():
                messages.error(request, 'Категория с этим названием уже существует.')
            else:
                form.save()
                messages.success(request, 'Категория успешно создана.')
                return redirect('money_tracker:add_expense')
    else:
        form = CategoryForm(user=request.user)
    return render(request, 'money_tracker/add_category.html', {'form': form})


@login_required
def expense_chart(request):
    expenses = Expense.objects.filter(user=request.user)
    # total_sum = sum([expense.amount for expense in expenses])
    # total_sum = Expense.objects.all().aggregate(Sum('amount'))['amount__sum']
    total_sum = expenses.aggregate(Sum('amount'))['amount__sum']

    category_totals = expenses.values('category__name').annotate(total=Sum('amount'))
    labels = [category['category__name'] for category in category_totals]
    amounts = [category['total'] for category in category_totals]
    labels = [str(label) for label in labels]
    amounts = [str(amount) for amount in amounts]
    return render(request, 'money_tracker/expense_chart.html',
                  {'labels': json.dumps(labels), 'amounts': json.dumps(amounts), 'section': 'expense_chart',
                   'total_sum': total_sum})


@login_required
def calculate_total_expenses_without_category(request, category_name):
    expenses_without_category = Expense.objects.filter(user=request.user).exclude(category__name=category_name)
    total_sum_without_category = expenses_without_category.aggregate(Sum('amount'))['amount__sum']
    return JsonResponse({'total_sum_without_category': total_sum_without_category})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense,
                                id=pk)
    form = ExpenseForm(instance=expense)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('money_tracker:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'money_tracker/edit_expense.html', {'form': form})
