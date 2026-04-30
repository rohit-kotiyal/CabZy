from rest_framework import serializers
from .models import Ride


class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'pickup_lat', 'pickup_lng', 'pickup_address',
            'drop_lat',   'drop_lng',   'drop_address',
        ]
    

class RideSerializer(serializers.ModelSerializer):
    rider_email = serializers.EmailField(source='rider.email', read_only=True)
    driver_email = serializers.EmailField(source='driver.user.email', read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id', 'rider_email', 'driver_email', 'status',
            'pickup_lat', 'pickup_lng', 'pickup_address',
            'drop_lat',   'drop_lng',   'drop_address',
            'distance_km', 'fare',
            'cancelled_by', 'cancel_reason',
            'created_at', 'started_at', 'completed_at',
        ]


class FareEstimateSerializer(serializers.Serializer):
    pickup_lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    pickup_lng = serializers.DecimalField(max_digits=9, decimal_places=6)
    drop_lat   = serializers.DecimalField(max_digits=9, decimal_places=6)
    drop_lng   = serializers.DecimalField(max_digits=9, decimal_places=6)
    vehicle_type = serializers.ChoiceField(choices=['BIKE', 'AUTO', 'CAR', 'SUV'])