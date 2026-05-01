from django.urls import path
from views import ToggleAvailibilityView, PendingRideView, AcceptRideView, RejectRideView


urlpatterns = [
    path('availability/', ToggleAvailibilityView.as_view(), name='toggle_availability'),
    path('rides/pending/', PendingRideView.as_view(), name='pending_rides'),
    path('rides/<int:pk>/accept/', AcceptRideView.as_view(), name='accept_ride'),
    path('rides/<int:pk>/reject/', RejectRideView.as_view(), name='reject_ride'),
]