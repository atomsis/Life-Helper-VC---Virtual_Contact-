import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserBalance, Transaction
from .forms import SendMoneyForm, DepositForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from decimal import Decimal


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def send_money(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            amount = Decimal(form.cleaned_data['amount'])
            sender_balance = UserBalance.objects.get_or_create(user=request.user)[0]
            receiver_balance = UserBalance.objects.get_or_create(user=friend)[0]

            if sender_balance.balance >= amount:
                sender_balance.balance -= amount
                receiver_balance.balance += amount
                sender_balance.save()
                receiver_balance.save()
                Transaction.objects.create(sender=request.user, receiver=friend, amount=amount)
                return redirect('finance:success')
            else:
                # Если баланс недостаточный, верните ошибку или сообщение
                form.add_error(None, "Недостаточно средств на счете.")
    else:
        form = SendMoneyForm()
    return render(request, 'finance/send_money.html', {'form': form, 'friend': friend})


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Сохранение суммы как строку в сессию
            request.session['deposit_amount'] = str(amount)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Account Deposit',
                        },
                        'unit_amount': int(amount * 100),  # amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/finance/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/finance/cancel/'),
            )
            # user_balance = UserBalance.objects.get(user=request.user)
            # user_balance += amount
            # user_balance.save()
            # return redirect('success')
            return redirect(session.url, code=303)
    else:
        form = DepositForm()
    return render(request, 'finance/deposit.html', {'form': form, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

def success(request):
    session_id = request.GET.get('session_id')

    if session_id:
        # Обработка пополнения баланса через Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        amount = Decimal(session['amount_total']) / 100

        user_balance, created = UserBalance.objects.get_or_create(user=request.user)
        user_balance.balance += amount
        user_balance.save()

        return render(request, 'finance/success_deposit.html', {'amount': amount, 'type': 'deposit'})
    else:
        # Обработка успешной отправки денег другу
        # Предполагаем, что у нас есть информация о последней транзакции пользователя
        transaction = Transaction.objects.filter(sender=request.user).order_by('-timestamp').first()
        if transaction:
            friend_name = transaction.receiver.username
            amount = Decimal(transaction.amount)
        else:
            friend_name = 'Unknown'
            amount = 0

        return render(request, 'finance/success_friend.html', {
            'type': 'send_money',
            'friend_name': friend_name,
            'amount': amount
        })


@login_required
def cancel(request):
    # Получаем сумму из сессии и преобразуем обратно в Decimal
    amount_str = request.session.pop('deposit_amount', '0')
    amount = Decimal(amount_str)

    return render(request, 'finance/cancel.html', {'amount': amount})
