from decimal import Decimal
import math
import requests
from django.conf import settings
# Coordenadas del punto de referencia
COORD_REFERENCIA = {
    'lat': 19.953220868549767,
    'lng': -99.53760337575697
}

# Tarifa base y por km adicional
TARIFA_BASE = Decimal('20.00')
TARIFA_KM_ADICIONAL = Decimal('5.00')

# Radio de cobertura para tarifa base (en km)
RADIO_COBERTURA = 2
def validar_direccion(direccion):
    """Valida la dirección usando la API de Address Validation de Google Maps"""
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={api_key}"
    
    # Formatear la dirección para la API
    address_data = {
        "address": {
            "regionCode": "MX",
            "addressLines": [
                f'{direccion["street"]} {direccion["number"]}',
                f'{direccion["neighborhood"]}, {direccion["zip_code"]}',
                f'{direccion["city"]}, {direccion["state"]}'
            ]
        }
    }
    
    response = requests.post(url, json=address_data)
    
    print("Respuesta completa de la API:")
    print(response.json())  # Imprime la respuesta completa en la consola

    if response.status_code == 200:
        result = response.json()
        
        # Verificar si la dirección se validó correctamente
        if result.get('result', {}).get('verdict', {}).get('validationGranularity') != 'UNCONFIRMED_BUT_PLAUSIBLE':
            print("hola bebe como has estado")
            return result.get('result', {})
    
    return None


def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia lineal entre dos puntos usando la fórmula de Haversine"""
    R = 6371  # Radio de la Tierra en km
    
    # Convertir coordenadas a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Diferencias de coordenadas
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia = R * c

    print(f"\n Distancia lineal {distancia}")
    
    return distancia

def get_route_distance( origin, destination):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters"
    }
    payload = {
        "origin": {"location": {"latLng": {"latitude": origin[0], "longitude": origin[1]}}},
        "destination": {"location": {"latLng": {"latitude": destination[0], "longitude": destination[1]}}},
        "travelMode": "DRIVE"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and data["routes"]:
            return data["routes"][0]["distanceMeters"] / 1000  # Convertir metros a km
        else:
            return "No se encontró una ruta."
    else:
        return f"Error en la solicitud: {response.status_code}, {response.text}"

def calcular_costo_envio(latitud, longitud):
    """Calcula el costo de envío basado en la distancia"""

    print(f"\n Latitud: {latitud} \n Longitud: {longitud}")
    # Calcular distancia lineal
    distancia_lineal = calcular_distancia_haversine(
        latitud, longitud,
        COORD_REFERENCIA['lat'], COORD_REFERENCIA['lng']
    )
    
    
    # Si está dentro del radio de cobertura, cobrar tarifa base
    if distancia_lineal <= RADIO_COBERTURA:
        print(f"\nEl costo total es: {TARIFA_BASE} ")
        return TARIFA_BASE
    else:
        # Si está fuera, calcular distancia por carretera y aplicar tarifa adicional
        distancia_carretera = get_route_distance(
            (latitud, longitud),
            (COORD_REFERENCIA['lat'], COORD_REFERENCIA['lng'])
        )
        print(f"\nDistancia en carretera {distancia_carretera}")
        
        # Calcular kilómetros extras (redondeando hacia arriba)
        km_extras = math.ceil(distancia_carretera - RADIO_COBERTURA)
        
        # Calcular costo total
        costo_total = TARIFA_BASE + (TARIFA_KM_ADICIONAL * Decimal(str(km_extras)))
        
        print(f"\nEl costo total es: {costo_total} ")
        return costo_total