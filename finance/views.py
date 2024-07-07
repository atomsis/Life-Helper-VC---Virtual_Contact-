from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserBalance, Transaction
from .forms import SendMoneyForm, DepositForm
from django.contrib.auth.decorators import login_required


@login_required
def send_money(request,friend_id):
    friend = get_object_or_404(User, id=friend_id)
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            sender_balance = UserBalance.objects.get(user=request.user)
            receiver_balance = UserBalance.objects.get(user=friend)
            if sender_balance >= amount:
                sender_balance -= amount
                receiver_balance += amount
                sender_balance.save()
                receiver_balance.save()
                Transaction.objects.create(sender=request.user, receiver=friend, amount=amount)
                return redirect('success')
    else:
        form = SendMoneyForm()
    return render(request, 'finance/send_money.html', {'form': form, 'friend': friend})


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_balance = UserBalance.objects.get(user=request.user)
            user_balance += amount
            user_balance.save()
            return redirect('success')
    else:
        form = DepositForm()
    return render(request, 'finance/deposit.html', {'form': form})
