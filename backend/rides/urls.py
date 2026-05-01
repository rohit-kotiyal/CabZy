from django.urls import path
from .views import FareEstimateView, RideView, RideDetailView, StartRideView, CompleteRideView, CancelRideView


urlpatterns = [
    path('estimate/', FareEstimateView.as_view(), name='fare_estimate'),
    path('', RideView.as_view(), name='rides'),
    path('<int:pk>/', RideDetailView.as_view(), name='ride_detail'),
    path('<int:pk>/start/', StartRideView.as_view(), name='start_ride'),
    path('<int:pk>/complete/', CompleteRideView.as_view(), name='complete_ride'),
    path('<int:pk>/cancel', CancelRideView.as_view(), name='cancel_ride'),
]

