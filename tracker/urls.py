from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard as homepage
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    path('update/<int:expense_id>/', views.update_expense, name='update_expense'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
