from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm
from django.db.models import Sum


# Register a new user
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})


# Log in a user
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'tracker/login.html')


# Log out a user
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


# Dashboard View
@login_required
def dashboard(request):
    """Display user dashboard with total budget, spent amount, and transactions."""
    budget = Budget.objects.get_or_create(user=request.user)[
        0]   # Ensure budget exists
    expenses = Expense.objects.filter(user=request.user)

    total_budget = budget.total_budget if budget else 0
    total_spent = expenses.aggregate(Sum('amount'))[
        'amount__sum'] or 0  # Sum of all expenses
    budget_left = total_budget - total_spent
    total_transactions = expenses.count()

    # Get sorting parameter from request
    sort_option = request.GET.get("sort", "date_asc")

    # Apply sorting
    if sort_option == "date_asc":
        expenses = expenses.order_by("date")  # Oldest first
    elif sort_option == "date_desc":
        expenses = expenses.order_by("-date")  # Newest first
    elif sort_option == "category_asc":
        expenses = expenses.order_by("category")  # A-Z
    elif sort_option == "category_desc":
        expenses = expenses.order_by("-category")  # Z-A

    context = {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "budget_left": budget_left,
        "total_transactions": total_transactions,
        "expenses": expenses,
        "selected_sort": sort_option,
    }
    return render(request, 'tracker/dashboard.html', context)


# Set or update budget
@login_required
def set_budget(request):
    """Handles setting or updating the user's budget"""
    budget, _ = Budget.objects.get_or_create(user=request.user)

    if request.method == "POST":
        budget.total_budget = request.POST['total_budget']
        budget.save()
        return redirect('dashboard')  # Redirect back to the dashboard
    return render(request, 'tracker/dashboard.html', {'total_budget': budget.total_budget})


# List expenses
@login_required
def expense_list(request):
    """Display all expenses."""
    expenses = Expense.objects.filter(
        user=request.user)  # Show only user's expenses

    # Get sorting parameter from request
    sort_option = request.GET.get("sort", "")

    # Apply sorting
    if sort_option == "date_asc":
        expenses = expenses.order_by("date")  # Oldest first
    elif sort_option == "date_desc":
        expenses = expenses.order_by("-date")  # Newest first
    elif sort_option == "category_asc":
        expenses = expenses.order_by("category")  # A-Z
    elif sort_option == "category_desc":
        expenses = expenses.order_by("-category")  # Z-A

    return render(request, 'tracker/expense_list.html', {'expenses': expenses})


# Add new expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        Expense.objects.create(user=request.user, category=category,
                               amount=amount, description=description, date=date)
        return redirect('dashboard')
    return render(request, 'tracker/dashboard.html')


# Update an expense
@login_required
def update_expense(request, expense_id):
    """Handle updating an expense"""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.category = request.POST['category']
        expense.amount = request.POST['amount']
        expense.description = request.POST['description']
        expense.date = request.POST['date']
        expense.save()
        return redirect('dashboard')  # Redirect to dashboard after update
    return render(request, 'tracker/dashboard.html', {'expense': expense})


# Delete an expense
@login_required
def delete_expense(request, expense_id):
    """Handle deleting an expense."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('dashboard')  # Redirect to dashboard after deletion
    return render(request, 'tracker/dashboard.html', {'expense': expense})
