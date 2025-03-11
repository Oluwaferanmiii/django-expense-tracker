from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Project
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
            return redirect('project_page')  # Redirect to the project page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'tracker/login.html')


# Log out a user
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


# Project Page: Display all projects and allow adding new ones
@login_required
def project_page(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'tracker/projects.html', {'projects': projects})


# Add a new project (handled via modal)
@login_required
def add_project(request):
    if request.method == "POST":
        name = request.POST['name']
        budget = request.POST['budget']
        project = Project.objects.create(
            user=request.user, name=name, budget=budget)
        # Redirect to project dashboard
        return redirect('dashboard', project_id=project.id)
    return render(request, 'tracker/projects.html')


# Dashboard now filters expenses by project
@login_required
def dashboard(request, project_id):
    """Display a project-specific dashboard"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    expenses = Expense.objects.filter(project=project)

    total_budget = project.budget
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    budget_left = total_budget - total_spent
    total_transactions = expenses.count()

    sort_option = request.GET.get("sort", "date_asc")

    # Apply sorting
    if sort_option == "date_asc":
        expenses = expenses.order_by("date")
    elif sort_option == "date_desc":
        expenses = expenses.order_by("-date")
    elif sort_option == "category_asc":
        expenses = expenses.order_by("category")
    elif sort_option == "category_desc":
        expenses = expenses.order_by("-category")

    context = {
        "project": project,
        "total_budget": total_budget,
        "total_spent": total_spent,
        "budget_left": budget_left,
        "total_transactions": total_transactions,
        "expenses": expenses,
        "selected_sort": sort_option,
    }
    return render(request, 'tracker/dashboard.html', context)


# List expenses
@login_required
def expense_list(request, project_id):
    """Display all expenses for a specific project."""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    expenses = Expense.objects.filter(project=project)

    sort_option = request.GET.get("sort", "")

    # Apply sorting
    if sort_option == "date_asc":
        expenses = expenses.order_by("date")
    elif sort_option == "date_desc":
        expenses = expenses.order_by("-date")
    elif sort_option == "category_asc":
        expenses = expenses.order_by("category")
    elif sort_option == "category_desc":
        expenses = expenses.order_by("-category")

    return render(request, 'tracker/expense_list.html', {'expenses': expenses, 'project': project})


# Add new expense now associates with a project
@login_required
def add_expense(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        Expense.objects.create(project=project, category=category,
                               amount=amount, description=description, date=date)
        return redirect('dashboard', project_id=project.id)

    return render(request, 'tracker/dashboard.html', {'project': project})


# Update an expense
@login_required
def update_expense(request, project_id, expense_id):
    """Handle updating an expense inside a specific project"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    expense = get_object_or_404(Expense, id=expense_id, project=project)

    if request.method == 'POST':
        expense.category = request.POST['category']
        expense.amount = request.POST['amount']
        expense.description = request.POST.get('description', '')
        expense.date = request.POST['date']
        expense.save()
        # Redirect back to project dashboard
        return redirect('dashboard', project_id=project.id)

    return render(request, 'tracker/dashboard.html', {'expense': expense, 'project': project})


# Delete an expense
@login_required
def delete_expense(request, project_id, expense_id):
    """Handle deleting an expense."""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    expense = get_object_or_404(
        Expense, id=expense_id, project__user=request.user)

    if request.method == "POST":
        expense.delete()
        # Redirect to the correct project dashboard
        return redirect('dashboard', project_id=project.id)

    return render(request, 'tracker/dashboard.html', {'expense': expense, 'project': project})


# Delete a project
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        project.delete()
        return redirect('project_page')  # Redirect to project selection
    return render(request, 'tracker/projects.html', {'project': project})
