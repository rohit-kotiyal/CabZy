from django.urls import path
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, MeView, RiderProfileView, DriverProfileView



RateLimitedLoginView = method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='post')(TokenObtainPairView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', RateLimitedLoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_view'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('profile/rider/', RiderProfileView.as_view(), name='rider_profile'),
    path('profile/driver/', DriverProfileView.as_view(), name='driver_profile'),
]
