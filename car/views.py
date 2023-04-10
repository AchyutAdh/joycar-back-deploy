from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Appointment, Car, Auction, Bid
from rest_framework.exceptions import ValidationError
from .serializers import AppointmentSerializer, BidAllSerializer, CarSerializer, AuctionSerializer, BidSerializer
from rest_framework.exceptions import NotFound

class CarCreateAPIView(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]



class AuctionCreateAPIView(generics.CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        car_id = request.data.get('car_id')
        price = request.data.get('price')
        duration = request.data.get('duration')
        if not car_id or not price or not duration:
            return Response({'error': 'car_id, price, and duration are required fields'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'car with id {} does not exist'.format(car_id)}, status=status.HTTP_404_NOT_FOUND)
        if car.status != 'active':
            return Response({'error': 'car with id {} is not active'.format(car_id)}, status=status.HTTP_400_BAD_REQUEST)
        end_time = timezone.now() + timezone.timedelta(minutes=duration)
        auction = Auction.objects.create(car=car, price=price, end_time=end_time)
        serializer = self.get_serializer(auction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class BidCreateAPIView(generics.CreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        auction_id = self.kwargs.get('pk')
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise ValidationError("Auction does not exist")

        if auction.end_time < timezone.now():
            raise ValidationError("Auction has ended")

        if serializer.validated_data['price'] <= auction.price:
            raise ValidationError("Bid price must be higher than current price")

        serializer.save(user=self.request.user, auction=auction)

        # Update the active bidder on the auction
        auction.active_bidder = self.request.user
        auction.price = serializer.validated_data['price']
        auction.save()

        # Serialize the updated auction data and return it in the response
        serializer = AuctionSerializer(auction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ActiveAuctionListAPIView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Auction.objects.filter(end_time__gt=timezone.now(), car__status='active')
    

class AuctionDetailAPIView(generics.RetrieveAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]


class BidListAPIView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        try:
            auction_id = self.kwargs['pk']
            bids = Bid.objects.filter(auction_id=auction_id)
        except Bid.DoesNotExist:
            raise NotFound("Bids do not exist for this auction")
        return bids
    
class BidListAllAPIView(generics.ListAPIView):
    serializer_class = BidAllSerializer
    queryset = Bid.objects.all()
   

class UserWonAuctionsAPIView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Auction.objects.filter(winner_id=user_id)
    
class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentListAPIView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]
    

class AuctionsByUserAPIView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Auction.objects.filter(car__user_id=user_id, car__status='active')