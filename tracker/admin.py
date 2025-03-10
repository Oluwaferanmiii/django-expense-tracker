from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'amount', 'description', 'date')
    list_filter = ('category', 'date')  # Allows filtering by category and date
    search_fields = ('category', 'description')  # Enables search functionality
    ordering = ('-date', )    # Orders expenses by most recent date
    date_hierarchy = 'date'   # Adds a date-based navigation filter


admin.site.register(Expense, ExpenseAdmin)
