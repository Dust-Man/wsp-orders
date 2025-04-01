from datetime import datetime
from django.utils import timezone
from shop.models import StoreStatus  # Ajusta la importación según tu estructura

def store_hours(request):
    """
    Contexto que determina si la tienda está abierta según horarios de operación
    y el estado manual de la tienda.
    """
    now = timezone.localtime(timezone.now())
    day_of_week = now.weekday()  # 0-6 (lunes a domingo)
    # day_of_week = 1

    current_time = now.time()

    hora_str = "15:39:05.579791"
    formato = "%H:%M:%S.%f"  # Formato con microsegundos

    hora_time = datetime.strptime(hora_str, formato).time()
    current_time = hora_time

    print(f"now: {now} \nday_of_w: {day_of_week} \ncurrent_time; {current_time}")
    
    # Obtenemos el estado actual de la tienda
    store_status = StoreStatus.get_status()
    
    # Si hay un cierre manual, la tienda está cerrada independientemente del horario
    if store_status.manual_override and not store_status.is_open:
        return {
            'store_open': False,
            'closed_reason': store_status.closed_reason or "Tienda cerrada temporalmente",
            'manual_override': True
        }
    
    # Horarios de operación
    # Lunes a sábado (0-5): 8:00 a 17:00
    # Domingo (6): 8:00 a 16:00
    is_within_hours = False
    
    if day_of_week < 6:  # Lunes a sábado
        start_time = timezone.datetime.strptime("08:00", "%H:%M").time()
        end_time = timezone.datetime.strptime("17:00", "%H:%M").time()
        is_within_hours = start_time <= current_time <= end_time
    else:  # Domingo
        start_time = timezone.datetime.strptime("08:00", "%H:%M").time()
        end_time = timezone.datetime.strptime("16:00", "%H:%M").time()
        is_within_hours = start_time <= current_time <= end_time
    
    # Si no estamos en horario de operación, la tienda está cerrada
    if not is_within_hours:
        return {
            'store_open': False,
            'closed_reason': "Fuera del horario de atención",
            'manual_override': False
        }
    
    # En horario de operación, la tienda está abierta
    return {
        'store_open': True,
        'closed_reason': None,
        'manual_override': False
    }