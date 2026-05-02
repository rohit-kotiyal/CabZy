from django.urls import path
from .views import PaymentDetailView, PromoValidateView


urlpatterns = [
    path('rides/<int:ride_id>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('promo/validate/', PromoValidateView.as_view(), name='promo_validate'),
]
