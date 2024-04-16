from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.contrib.auth.decorators import login_required


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    # expenses = Expense.objects.all()

    return render(request, 'money_tracker/expense_list.html', {'expenses': expenses,'section': 'expense_list'})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('money_tracker:expense_list')
    else:
        form = ExpenseForm()
    return render(request,'money_tracker/add_expense.html',{'form':form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('money_tracker:add_expense')
    else:
        form = CategoryForm()
    return render(request, 'money_tracker/add_category.html', {'form': form})

@login_required
def expense_chart(request):
    expenses = Expense.objects.filter(user=request.user)
    category_totals = expenses.values('category__name').annotate(total=Sum('amount'))
    labels = [category['category__name'] for category in category_totals]
    amounts = [category['total'] for category in category_totals]
    return render(request, 'money_tracker/expense_chart.html', {'labels': labels, 'amounts': amounts,'section': 'expense_chart'})


@login_required
def edit_expense(requset):
    expense = get