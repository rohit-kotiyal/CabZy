from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import empty

from .models import Ride
from .serializers import RideCreateSerializer, RideSerializer, FareEstimateSerializer
from .services import calculate_fare, estimate_distance


# Create your views here.
class FareEstimateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FareEstimateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if not data:
                return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

            dist = estimate_distance(data['pickup_lat'], data['pickup_lng'], data['drop_lat'], data['drop_lng'])
            fare = calculate_fare(dist, data['vehicle_type'])
            return Response({"estimated_fare": fare, "distance_km": dist})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RideView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_rider:
            rides = Ride.objects.filter(rider=request.user).order_by('-created_at')
        elif request.user.is_cab_admin:
            rides = Ride.objects.all().order_by('-created_at')
        else:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        return Response(RideSerializer(rides, many=True).data)

    def post(self, request):
        if not request.user.is_rider:
            return Response({"detail": "Only riders can request rides."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RideCreateSerializer(data=request.data)
        if serializer.is_valid():
            d    = serializer.validated_data
            dist = estimate_distance(d['pickup_lat'], d['pickup_lng'], d['drop_lat'], d['drop_lng'])
            fare = calculate_fare(dist, 'CAR')

            ride = Ride.objects.create(
                rider       = request.user,
                distance_km = dist,
                fare        = fare,
                **d
            )
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RideDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ride = Ride.objects.get(pk=pk)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        # riders can only see their own rides
        if request.user.is_rider and ride.rider != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        return Response(RideSerializer(ride).data)