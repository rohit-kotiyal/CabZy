from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rides.models import Ride
from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerializer


class ReviewCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        if not (request.user.is_rider or request.user.is_driver):
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            d: dict = serializer.validated_data
            ride = Ride.objects.get(pk=d['ride_id'])

            # rider reviews driver, drivers review rider

            if request.user.is_rider:
                if ride.rider != request.user:
                    return Response({"detail": "Not your ride."}, status=status.HTTP_403_FORBIDDEN)
                rated_user = ride.driver.user 
            else:
                if ride.driver.user != request.user:
                    return Response({"detail": "Not your ride."}, status=status.HTTP_403_FORBIDDEN)
                rated_user = ride.rider

            review = Review(
                ride = ride,
                rated_by = request.user,
                rated_user = rated_user,
                rating = d['rating'],
                comment = d.get('comment', '')
            )

            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        try:
            ride = Ride.objects.get(pk=ride_id)
            review = ride.review
        except Ride.DoesNotExist:
            return Response({"detail": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)
        except Review.DoesNotExist:
            return Response({"detail": "No review for this ride yet."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(ReviewSerializer(review).data)


class UserReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.filter(rated_user=request.user).order_by('-created_at')
        return Response(ReviewSerializer(reviews, many=True).data)
