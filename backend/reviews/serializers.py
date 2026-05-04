from rest_framework import serializers
from .models import Review
from rides.models import Ride



class ReviewCreateSerializer(serializers.ModelSerializer):
    ride_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['ride_id', 'rating', 'comment']


    def validate_ride_id(self, value):
        try:
            ride = Ride.objects.get(pk=value)
        except Ride.DoesNotExist:
            raise serializers.ValidationError('Ride not found.!')
        
        if ride.status != Ride.Status.COMPLETED:
            raise serializers.ValidationError("You can only review a completed ride.")
        
        if hasattr(ride, 'review'):
            raise serializers.ValidationError("This ride has already been reviewed.")
        
        return value
    

class ReviewSerializer(serializers.ModelSerializer):
    rated_by = serializers.EmailField(source='rated_by.email', read_only=True)
    rated_user = serializers.EmailField(source='rated_user.email', read_only=True)
    ride_id = serializers.IntegerField(source='ride.id', read_only=True)


    class Meta:
        model = Review
        fields = ['id', 'ride_id', 'rated_by', 'rated_user', 'rating', 'comment', 'created_at']