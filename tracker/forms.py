from django import forms
from .models import Expense, Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['total_budget']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
