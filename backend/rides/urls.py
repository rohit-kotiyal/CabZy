from django.urls import path
from .views import FareEstimateView, RideView, RideDetailView


urlpatterns = [
    path('estimate/', FareEstimateView.as_view(), name='fare_estimate'),
    path('', RideView.as_view(), name='rides'),
    path('<int:ride_id>/', RideDetailView.as_view(), name='ride_detail'),
]

