from django.urls import path
from .views import ReviewCreateView, ReviewDetailView, UserReviewsView


urlpatterns = [
    path('', ReviewCreateView.as_view(), name='review_create'),
    path('rides/<int:ride_id>/', ReviewDetailView.as_view(), name='review_detail'),
    path('mine/', UserReviewsView.as_view(), name='my_reviews'),
]
