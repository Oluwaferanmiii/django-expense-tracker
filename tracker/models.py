from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_budget = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def budget_left(self):
        total_spent = Expense.objects.filter(user=self.user).aggregate(
            models.Sum('amount'))['amount__sum'] or 0
        return self.total_budget - total_spent


class Expense(models.Model):
    # Temporarily allow null values
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, default='Untitled Expense')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: {self.amount}"
