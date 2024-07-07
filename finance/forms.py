from django import forms
from django.contrib.auth.models import User
from .models import UserBalance


class SendMoneyForm(forms.Form):
    receiver_username = forms.CharField(max_length=150)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_receiver_username(self):
        username = self.cleaned_data.get('receiver_username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь не существует.")
        return username

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть положительной.")
        return amount


class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть положительной.")
        return amount
