from django.contrib import admin
from .models import Expense, Category


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    fields = ['user', 'amount', 'date', 'category', 'description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['user','name']

