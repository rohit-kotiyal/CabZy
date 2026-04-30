import requests
from decimal import Decimal
from config.settings import ORS_API_KEY


# rate for vehicle type

RATES = {
    'BIKE': Decimal('8.00'),
    'AUTO': Decimal('12.00'),
    'CAR': Decimal('16.00'),
    'SUV': Decimal('22.00'),
}

BASE_FARE = Decimal('30.00')
MIN_FARE = Decimal('50.00')



def estimate_distance(pickup_lat, pickup_lng, drop_lat, drop_lng) -> float:
    
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [
            [float(pickup_lng), float(pickup_lat)],  # ORS takes [lng, lat]
            [float(drop_lng),   float(drop_lat)]
        ]
    }


    try:
        response = requests.post(url, json=body, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        distance_meters = data['routes'][0]['summary']['distance']

        return round(distance_meters/1000, 2)  # convert to km

    except Exception:
        return _haversine_fallback(pickup_lat, pickup_lng, drop_lat, drop_lng)



def _haversine_fallback(pickup_lat, pickup_lng, drop_lat, drop_lng) -> float:
    import math
    R    = 6371
    lat1 = math.radians(float(pickup_lat))
    lat2 = math.radians(float(drop_lat))
    dlat = math.radians(float(drop_lat) - float(pickup_lat))
    dlng = math.radians(float(drop_lng) - float(pickup_lng))
    a    = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    c    = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * c * 1.35, 2)



def calculate_fare(distance_km: float, vehicle_type: str) -> Decimal:
    distance = Decimal(str(distance_km))
    rate     = RATES.get(vehicle_type, RATES['CAR'])
    fare     = BASE_FARE + (distance * rate)
    return max(fare, MIN_FARE)
