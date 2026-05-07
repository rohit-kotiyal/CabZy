from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.fields import empty

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from payments.models import Payment
from .models import Ride
from .serializers import RideCreateSerializer, RideSerializer, FareEstimateSerializer
from .services import calculate_fare, estimate_distance

from notifications.sevices import send_notification
from notifications.models import Notification


# helper function
def push_ride_status(ride_id, new_status):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"ride_{ride_id}",
        {
            'type': 'ride_status_update',
            'status': new_status,
        }
    )



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
    


class StartRideView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can start rides."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ride = Ride.objects.get(pk=pk, driver=request.user.driver_profile)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)
        
        if ride.status != Ride.Status.ASSIGNED:
            return Response({"detail": f"Cannot start a ride with status '{ride.status}'."}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = Ride.Status.IN_PROGRESS
        ride.started_at = timezone.now()
        ride.save()

        push_ride_status(ride.id, ride.status)

        send_notification(
            user=ride.rider,
            type=Notification.Type.RIDE_STARTED,
            title="Your ride has started",
            message="Your driver has started the ride. Hang tight!"
        )

        return Response(RideSerializer(ride).data)
    

class CompleteRideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can complete rides."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ride = Ride.objects.get(pk=pk, driver=request.user.driver_profile)

        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found or not assigned to you."}, status=status.HTTP_404_NOT_FOUND)
        
        if ride.status != Ride.Status.IN_PROGRESS:
            return Response({"detail": f"Cannot complete a ride with status '{ride.status}'."}, status=status.HTTP_400_BAD_REQUEST)
        
        ride.status = Ride.Status.COMPLETED
        ride.completed_at = timezone.now()
        ride.save()

        push_ride_status(ride.id, ride.status)

        # auto-create a pending payment record
        Payment.objects.get_or_create(
            ride = ride,
            defaults= [{
                'amount': ride.fare,
                'method': Payment.Method.CASH,
                'status': Payment.STATUS.PENDING
            }]
        )

        driver_profile = request.user.driver_profile
        driver_profile.is_available = False
        driver_profile.save()


        send_notification(
            user=ride.rider,
            type=Notification.Type.RIDE_COMPLETED,
            title="Ride Completed",
            message=f"Your ride is complete. Total Fare: Rs.{ride.fare}. Please leave a review!"
        )

        return Response(RideSerializer(ride).data)
    

class CancelRideView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        # both rider and driver can cancel
        if not (request.user.is_rider or request.user.is_driver):
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        try:
            if request.user.is_rider:
                ride = Ride.objects.get(pk=pk, rider=request.user)
            else:
                ride = Ride.objects.get(pk=pk, driver=request.user.driver_profile)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        # can only cancel if not already completed or cancelled
        if ride.status in [Ride.Status.COMPLETED, Ride.Status.CANCELLED]:
            return Response({"detail": f"Cannot cancel a ride with status '{ride.status}'."}, status=status.HTTP_400_BAD_REQUEST)

        ride.status       = Ride.Status.CANCELLED
        ride.cancelled_by = Ride.CancelledBy.RIDER if request.user.is_rider else Ride.CancelledBy.DRIVER
        ride.cancel_reason = request.data.get('reason', '')
        ride.save()

        push_ride_status(ride.id, ride.status)

        # notify the other party
        if request.user.is_rider and ride.driver:
            send_notification(
                user=ride.driver.user,
                type=Notification.Type.RIDE_CANCELLED,
                title="Ride Cancelled",
                message=f"Rider cancelled the ride. Reason: {ride.cancel_reason or 'No reason given'}"
            )

        return Response(RideSerializer(ride).data)
    


