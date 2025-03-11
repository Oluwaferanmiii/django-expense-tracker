from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def redirect_to_login_or_projects(request):
    if request.user.is_authenticated:
        # Redirect to project page if logged in
        return redirect('project_page')
    return redirect('login')  # Otherwise, go to login page


urlpatterns = [
    path('', redirect_to_login_or_projects, name='home'),
    path('projects/<int:project_id>/', views.dashboard,
         name='dashboard'),  # Dashboard as homepage
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Project management
    path('projects/', views.project_page, name='project_page'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/<int:project_id>/', views.dashboard, name='dashboard'),
    path('projects/<int:project_id>/delete/',
         views.delete_project, name='delete_project'),

    # Expenses within a project
    path('projects/<int:project_id>/expenses/add/',
         views.add_expense, name='add_expense'),
    path('projects/<int:project_id>/expenses/update/<int:expense_id>/',
         views.update_expense, name='update_expense'),
    path('projects/<int:project_id>/expenses/delete/<int:expense_id>/',
         views.delete_expense, name='delete_expense'),
    path('projects/<int:project_id>/expenses/',
         views.expense_list, name='expense_list'),

]
