from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('daily-sales/<str:date>/', views.daily_sales, name='daily_sales'),
    path('toggle-store-status/', views.toggle_store_status, name='toggle_store_status'),  # Nueva URL
]