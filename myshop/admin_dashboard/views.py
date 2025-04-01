from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, F
from django.contrib import messages
from datetime import datetime, timedelta
from orders.models import Order, OrderItem
import calendar
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import StoreStatus  # Ajusta según tu estructura

def is_superuser(user):
    return user.is_superuser

# Vista de login
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard:dashboard')
        else:
            messages.error(request, 'Credenciales inválidas o no tienes permisos de superusuario.')
    
    return render(request, 'admin_dashboard/login.html')

# Vista de logout
def admin_logout(request):
    logout(request)
    return redirect('admin_dashboard:login')

# Vista principal del dashboard
@user_passes_test(is_superuser, login_url='admin_dashboard:login')
def dashboard_view(request):
    today = timezone.now().date()
    
    # Obtener el estado actual de la tienda
    store_status = StoreStatus.get_status()
    
    # Redirigir a la vista de ventas diarias con el estado de la tienda
    response = daily_sales(request, today.strftime('%Y-%m-%d'))
    
    # Si la respuesta es un objeto HttpResponse (renderizado), añadir el estado de la tienda al contexto
    if hasattr(response, 'context_data'):
        response.context_data['store_status'] = store_status
    
    return response

# Vista para las ventas diarias
@user_passes_test(is_superuser, login_url='admin_dashboard:login')
def daily_sales(request, date):
    try:
        # Convertir la fecha de string a objeto date
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        # Si hay un error en el formato de fecha, usar la fecha actual
        selected_date = timezone.now().date()
        # Redirigir a la URL con la fecha correcta
        return redirect('admin_dashboard:daily_sales', date=selected_date.strftime('%Y-%m-%d'))
    
    today = timezone.now().date()
    
    # Definir el rango del día (inicio y fin)
    day_start = datetime.combine(selected_date, datetime.min.time())
    day_end = datetime.combine(selected_date, datetime.max.time())
    
    # Filtrar órdenes del día seleccionado y que estén enviadas (sent=True)
    daily_orders = Order.objects.filter(
        created__range=(day_start, day_end),
        sent=True
    )
    
    # Calcular total de ventas
    total_sales = daily_orders.aggregate(
        total=Sum(F('items__price') * F('items__quantity'))
    )['total'] or 0
    
    # Calcular total de envíos
    total_shipping = daily_orders.aggregate(
        total=Sum('shipping_cost')
    )['total'] or 0
    
    # Obtener todas las órdenes del día (para el resumen)
    all_daily_orders = Order.objects.filter(
        created__range=(day_start, day_end), #MARCADOR###
      
    ).order_by('-created')
    
    # Crear datos para el calendario
    current_month = selected_date.month
    current_year = selected_date.year
    
    # Obtener el primer día del mes y el número de días
    month_calendar = calendar.monthcalendar(current_year, current_month)
    
    # Nombre del mes
    month_name = calendar.month_name[current_month]
    
    # Para navegación entre meses
    prev_month = selected_date.replace(day=1) - timedelta(days=1)
    next_month = (selected_date.replace(day=28) + timedelta(days=7)).replace(day=1)
    
    store_status = StoreStatus.get_status()

    context = {
        'selected_date': selected_date,
        'total_sales': total_sales,
        'total_shipping': total_shipping,
        'orders': all_daily_orders,
        'month_calendar': month_calendar,
        'month_name': month_name,
        'year': current_year,
        'prev_month': prev_month,
        'next_month': next_month,
        'today': today, 
        'store_status': store_status,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)

@user_passes_test(is_superuser, login_url='admin_dashboard:login')
@require_POST
def toggle_store_status(request):
    """Vista para abrir/cerrar la tienda manualmente desde el panel de administración."""
    status = StoreStatus.get_status()
    
    # Cambiar el estado actual
    status.is_open = not status.is_open
    status.manual_override = not status.is_open  # Solo activar override si estamos cerrando
    
    # Si estamos cerrando la tienda, guardar el motivo
    if not status.is_open:
        status.closed_reason = request.POST.get('reason', 'Cerrado temporalmente')
    else:
        status.closed_reason = None
        
    status.save()
    
    return JsonResponse({
        'success': True,
        'is_open': status.is_open,
        'message': 'Tienda abierta' if status.is_open else 'Tienda cerrada'
    })