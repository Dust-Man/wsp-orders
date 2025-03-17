from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path("calculate-shipping/", views.calculate_shipping_cost, name="calculate_shipping_cost"),
 ]