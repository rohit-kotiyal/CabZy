from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminUser
from django.db.models import Count, Sum

from users.models import User, DriverProfile
from rides.models import Ride
from payments.models import Payment
from notifications.sevices import send_notification
from notifications.models import Notification



# User Management

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        role = request.query_params.get('role')
        users = User.objects.exclude(role=User.Role.ADMIN)

        if role:
            users = users.filter(role=role.upper())

        data = [
            {
                "id": u.id,
                "email": u.email,
                "phone": u.phone,
                "role": u.role,
                "is_active": u.is_active,
                "joined": u.date_joined,
            }
            for u in users.order_by('-date_joined')
        ]

        return Response(data)
    


class AdminBanUserView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user.is_cab_admin:
            return Response({"detail": "Cannot ban an admin."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = not user.is_active
        user.save()

        action = "unbanned" if user.is_active else "banned"

        return Response({"detail": f"User {action} successfully.", "is_active": user.is_active})



# Driver Management

class AdminPendingDriversView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        drivers = DriverProfile.objects.filter(is_approved=False).select_related('user')

        data = [
            {
                "id": d.id,
                "email": d.user.email,
                "phone": d.user.phone,
                "vehicle_type": d.vehicle_type,
                "vehicle_no": d.vehicle_no,
                "license_no": d.license_no,                
            }
            for d in drivers
        ]

        return Response(data)
    


class AdminApproveDriverView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            driver = DriverProfile.objects.get(pk=pk)
        except DriverProfile.DoesNotExist:
            return Response({"detail": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)
        
        driver.is_approved = True
        driver.save()

        send_notification(
            user = driver.user,
            type = Notification.Type.DRIVER_APPROVED,
            title = "Account Approved!",
            message = "Your driver account has been approved. You can now go online and accept rides." 
        )

        return Response({"detail": "Driver approved successfully."})
    


# Ride Monitoring
class AdminRideListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        ride_status = request.query_params.get('status')
        rides = Ride.objects.all().order_by('-created_at')

        if ride_status:
            rides = rides.filter(status=ride_status.upper())

        data = [
            {
                "id": r.id,
                "rider": r.rider.email if r.rider else None,
                "driver": r.driver.user.email if r.driver else None,
                "status": r.status,
                "fare": r.fare,
                "distance_km": r.distance_km,
                "created_at": r.created_at,
            }
            for r in rides
        ] 

        return Response(data)
    

# Analytics

class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_riders = User.objects.filter(role=User.Role.RIDER).count()
        total_drivers = User.objects.filter(role=User.Role.DRIVER).count()
        total_rides = Ride.objects.count()

        rides_by_status = Ride.objects.values('status').annotate(count=Count('id'))
        total_revenue = Payment.objects.filter(
            status=Payment.Status.PAID,
        ).aggregate(total=Sum('amount'))['total'] or 0

        active_drivers = DriverProfile.objects.filter(
            is_approved=True, is_available=True
        ).count()

        return Response({
            "total_riders": total_riders,
            "total_drivers": total_drivers,
            "total_rides": total_rides,
            "active_drivers": active_drivers,
            "total_revenue": total_revenue,
            "rides_bu_status": list(rides_by_status)
        })





