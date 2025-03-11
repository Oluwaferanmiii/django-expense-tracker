from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    """Represents a user-defined project for tracking expenses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="expenses", null=True)
    title = models.CharField(max_length=255, default='Untitled Expense')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.category}: {self.amount}"
