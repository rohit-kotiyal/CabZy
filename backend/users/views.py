from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import RiderProfile, DriverProfile
from .serializers import RegisterSerializer, UserSerializer, RiderProfileSerializer, DriverProfileSerializer



@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully.!"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid Token.!"}, status=status.HTTP_400_BAD_REQUEST)
        

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    


class RiderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_rider:
            return Response({"detail": "Not a rider."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.rider_profile
        return Response(RiderProfileSerializer(profile).data)
    
    def patch(self, request):
        if not request.user.is_rider:
            return Response({"detail": "Not a rider."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.rider_profile
        serializer = RiderProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DriverProfileView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        if not request.user.is_driver:
            return Response({"detail": "Not a driver."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.driver_profile

        return Response(DriverProfileSerializer(profile).data)
    
    def patch(self, request):
        if not request.user.is_driver:
            return Response({"detail": "Not a driver."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.driver_profile
        serializer = DriverProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
