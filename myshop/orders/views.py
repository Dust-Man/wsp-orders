from django.shortcuts import render
from django.conf import settings  # Asegúrate de tener configurado tu token en settings
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
import requests
from django.http import JsonResponse
from .models import Address
import random  # Simularemos un cálculo de costo de envío
from decimal import Decimal
from .shipping import *


def calculate_shipping_cost(request):
    if request.method == "POST":
        direccion ={
                "street": request.POST["street"],
                "number":request.POST["number"],
                "zip_code":request.POST["zip_code"],
                "neighborhood":request.POST["neighborhood"],
                "city":request.POST["city"],
                "state":request.POST["state"],
                "country":request.POST["country"],
                }

        direccion_validada = validar_direccion(direccion)
            
        if direccion_validada:
                # Obtener coordenadas de la dirección validada
                direccion["latitude"] = direccion_validada.get('geocode', {}).get('location', {}).get('latitude')
                direccion["longitude"] = direccion_validada.get('geocode', {}).get('location', {}).get('longitude')
                direccion["formattedAddress"] = direccion_validada.get('address', {}).get('formattedAddress')
                
                # Calcular costo de envío
                costo = calcular_costo_envio(direccion["latitude"], direccion["longitude"])
                
                
                
                return JsonResponse({"shipping_cost": float(round(costo, 2))})
        
    return JsonResponse({"error": "Datos inválidos"}, status=400)

def send_whatsapp_message(order_details, recipient_phone):
    url = "https://graph.facebook.com/v22.0/604364196090619/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "text",
        "text": {
            "body": f"{order_details}"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 2xx
    except requests.exceptions.RequestException as e:
        # Si hay algún error con la API de WhatsApp, renderiza fail.html
        print(f"Error al enviar mensaje: {e}")
        return False
    
    return True

from .models import Address

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                street=request.POST["street"],
                number=request.POST["number"],
                zip_code=request.POST["zip_code"],
                neighborhood=request.POST["neighborhood"],
                city=request.POST["city"],
                state=request.POST["state"],
                country=request.POST["country"],
                reference = request.POST["reference"]
            )
           #ESTA LINEA DA EL FALLO

            order = form.save(commit=False)
            order.address = address
            order.shipping_cost = float(request.POST.get("shipping_cost", 0))
            order.sent = False
            order.save()
            
            # Aquí se envía el pedido por WhatsApp con la dirección y el costo de envío
            order_details = f"Orden *#{order.id}* \nCliente: {order.first_name} {order.last_name} \nDirección: {order.address.street} {order.address.number}, {order.address.neighborhood}, {order.address.city}, {order.address.state}, {order.address.zip_code}, {order.address.country} \nCosto de Envío: ${order.shipping_cost} \nTeléfono: {order.tel} \n\nProductos:\n"
            
            for item in cart:
                order_details += f"- {item['product'].name} - {item['quantity']}{item['prefix']} x ${item['price']} = {item['total_price']}\n"

            total = Decimal(cart.get_total_price()) + Decimal(order.shipping_cost)
            order_details += f"*Total:* ${total} \nNotas del cliente: {order.notes}"

            recipient_phone = "525510097293"
            if send_whatsapp_message(order_details, recipient_phone):
                order.sent = True
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])

                cart.clear()
                return render(request, 'orders/order/created.html', {'order': order})
            else:
                order.sent = False
                order.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                return render(request, 'orders/order/fail.html')

    else:
        form = OrderCreateForm()
        total = cart.get_total_price() + 20
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form,'total':total })