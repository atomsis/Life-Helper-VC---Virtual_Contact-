from django import forms
from .models import Expense, Category
from django.forms import DateInput
import datetime

class DatePickerWidget(DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'description']
        #------------ v1 -----------------
        # widget = forms.SelectDateWidget(
        #     attrs={'class': 'form-control'}
        # )
        #--------------------------------
        #------------ v2 ----------------
        # widget = forms.DateInput(
        #     attrs={'type': 'date'}
        # )
        #-------------------------------
        #----------- v3 ----------------
        widgets = {
            'date': DatePickerWidget(),
        }
        #-------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['date'] = instance.date.strftime('%Y-%m-%d')
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
