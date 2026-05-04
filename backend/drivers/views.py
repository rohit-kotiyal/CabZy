from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rides.models import Ride
from rides.serializers import RideSerializer

from notifications.models import Notification
from notifications.sevices import send_notification


class ToggleAvailibilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can toggle availability."}, status=status.HTTP_403_FORBIDDEN) 
        
        profile = request.user.profile

        if not profile.is_approved:
            return Response({"detail": "Your profile is not approved yet."}, status=status.HTTP_403_FORBIDDEN)
        
        profile.is_available = not profile.is_available
        profile.save()

        return Response({
            "is_available": profile.is_available,
            "detail": "You are now online." if profile.is_available else "You are now offline."
        })
    

class PendingRideView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can view pending rides."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.profile

        if not profile.is_approved:
            return Response({"detail": "Your profile is not approved yet."}, status=status.HTTP_403_FORBIDDEN)
        
        if not profile.is_available:
            return Response({"detail": "You must be online to view pending rides."}, status=status.HTTP_403_FORBIDDEN)  
        

        # show only unassigned requested rides
        rides = Ride.objects.filter(status=Ride.Status.REQUESTED, driver=None).order_by('-created_at')

        return Response(RideSerializer(rides, many=True).data)
    

class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id, pk):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can accept rides."}, status=status.HTTP_403_FORBIDDEN)
        
        profile = request.user.profile

        if not profile.is_approved:
            return Response({"detail": "Your profile is not approved yet."}, status=status.HTTP_403_FORBIDDEN)
        if not profile.is_available:
            return Response({"detail": "You must be online to accept rides."}, status=status.HTTP_403_FORBIDDEN)
        

        try:
            ride = Ride.objects.get(pk=pk, status=Ride.Status.REQUESTED)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found or already accepted."}, status=status.HTTP_404_NOT_FOUND)
        
        # check if driver already has an active ride
        active_ride = Ride.objects.filter(driver=profile, status_in=[Ride.Status.ASSIGNED, Ride.Status.IN_PROGRESS]).exists()

        if active_ride:
            return Response({"detail": "You already have an active ride. Please complete it before accepting a new one."}, status=status.HTTP_400_BAD_REQUEST)  
        
        ride.driver = profile
        ride.status = Ride.Status.ASSIGNED
        ride.save()

        send_notification(
            user=ride.rider,
            type=Notification.Type.RIDE_ASSIGNED,
            title="Driver Assigned",
            message=f"Your driver is on the way! Vehicle: {profile.vehicle_type} — {profile.vehicle_no}"
        )

        return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
    

class RejectRideView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, pk):
        if not request.user.is_driver:
            return Response({"detail": "Only drivers can reject rides."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            ride = Ride.objects.get(pk=pk, status=Ride.Status.REQUESTED)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found or already accepted."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"detail": "Ride rejected. It remains available for other drivers."})
