from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from rides.models import Ride
from .models import Payment, PromoCode
from .serializers import PaymentSerializer, PromoValidateSerializer


class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = Ride.objects.get(pk=ride_id)
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
        

        # riders can only see their own rides payment
        if request.user.is_rider and ride.rider != request.user:
             return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        

        try:
            payment = ride.payment
        except Payment.DoesNotExist:
            return Response({"detail": "No payment record found."}, status=status.HTTP_404_NOT_FOUND)


        return Response(PaymentSerializer(payment).data)
    

class PromoValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seralizer = PromoValidateSerializer(data=request.data)

        if seralizer.is_valid():
            code = seralizer.validated_data['code']
            
            try:
                promo = PromoCode.objects.get(code=code)
            except PromoCode.DoesNotExist:
                return Response({"detail": "Invalid promo code."}, status=status.HTTP_404_NOT_FOUND)
            
            if not promo.is_valid():
                return Response({"detail": "Promo code is expired or used up."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'code': promo.code,
                'dicount_pct': promo.discount_pct,
                'message': f"Promo Code applied! You get {promo.discount_pct}% off."
            })
        
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

