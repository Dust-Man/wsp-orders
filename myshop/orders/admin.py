from django.contrib import admin
from .models import Order, OrderItem, Address

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name','business', 'email','tel',
 'address','notes',
 'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]
@admin.register(Address)
class OrderAdress(admin.ModelAdmin):
    list_display = ['id']

