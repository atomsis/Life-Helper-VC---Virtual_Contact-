from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'money_tracker_category'

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'money_tracker_expense'

    def __str__(self):
        return f'{self.category}(для теста посмотреть че за текст)'

    def get_absolute_url(self):
        return reverse('money_tracker:edit_expense',
                       args=[self.id])
