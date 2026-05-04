from django.urls import path
from .views import (
    AdminUserListView, AdminBanUserView,
    AdminPendingDriversView, AdminApproveDriverView,
    AdminRideListView, AdminAnalyticsView
)


urlpatterns = [
    # users
    path('users/', AdminUserListView.as_view(), name='admin_users'),
    path('users/<int:pk>/ban/', AdminBanUserView.as_view(), name='admin_ban_user'),

    # drivers
    path('drivers/pending/', AdminPendingDriversView.as_view(), name='admin_pending_drivers'),
    path('drivers/<int:pk>/approve/',   AdminApproveDriverView.as_view(),  name='admin_approve_driver'),

    # rides
    path('rides/',               AdminRideListView.as_view(),    name='admin_rides'),

    # analytics
    path('analytics/',           AdminAnalyticsView.as_view(),   name='admin_analytics'),
]


