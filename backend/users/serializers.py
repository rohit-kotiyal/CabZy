from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, RiderProfile, DriverProfile



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'role', 'password', 'password2']

    def validate_role(self, value):
        if value not in [User.Role.RIDER, User.Role.DRIVER]:
            raise serializers.ValidationError('Invalid role.')
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password do not match.!"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'role']



class RiderProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)


    class Meta:
        model = RiderProfile
        fields = ['email', 'phone', 'default_pickup']


class DriverProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = DriverProfile
        fields = ['email', 'phone', 'vehicle_type', 'vehicle_no', 'license_no', 'is_approved', 'is_available']
        read_only_fields = ['is_approved']  # only admin can change this