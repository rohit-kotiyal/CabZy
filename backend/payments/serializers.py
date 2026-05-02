from rest_framework import serializers
from .models import Payment, PromoCode



class PaymentSerializer(serializers.ModelSerializer):
    ride_id = serializers.IntegerField(source='ride.id', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'ride_id', 'amount', 'method', 'status', 'gateway_ref', 'created_at']
        read_only_fields = ['amount', 'status', 'gateway_ref']


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount_pct', 'expires_at', 'is_active']


class PromoValidateSerializer(serializers.Serializer):
    code = serializers.CharField()

    