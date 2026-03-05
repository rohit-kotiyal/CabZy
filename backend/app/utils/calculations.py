import math
from fastapi import HTTPException

def validate_coordinates(lat: float, lng: float):
    if not (-90 <= lat <= 90):
        raise HTTPException(status_code=400, detail="Invalid Latitude")
    if not (-90 <= lng <= 90):
        raise HTTPException(status_code=400, detail="Invalid Longitude")
    

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula.
    Returns distance in meters.
    """
    
    R = 6371000  # Earth's radius in meters

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    
    delta_lat = math.radians(lat2-lat1)
    delta_lng = math.radians(lng2-lng1)

    a = (math.sin(delta_lat / 2) **2 + 
        math.cos(lat1_rad) * math.cos(lat2_rad) *
        math.sin(delta_lng / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return round(R*c, 2)


def calculate_fare(distance_meters: float, distance_seconds: float) -> float:
    """
    Calculate fare for a ride.
    Returns fare in rupees.
    """
    BASE_FARE = 50.0
    RATE_PER_KM = 10.0
    RATE_PER_MIN = 2.0
    MINIMUM_FARE = 100

    distance_km = distance_meters / 1000
    duration_minutes = distance_seconds / 60

    total = BASE_FARE + (distance_km * RATE_PER_KM) + (duration_minutes * RATE_PER_MIN)

    return round(max(total, MINIMUM_FARE), 2)


def estimate_duration(distance_meters: float) -> float:
    """
    Estimate trip duration.
    Returns duration in seconds.
    """
    avg_speed_kmh = 30
    distance_km = distance_meters / 1000
    duration_hrs = distance_km / avg_speed_kmh

    return round(duration_hrs * 3600, 2)

