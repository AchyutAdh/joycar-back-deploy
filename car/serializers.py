from rest_framework import serializers
from .models import Appointment, Car, Auction, Bid

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['id', 'name', 'model', 'year', 'description', 'price', 'image', 'status', 'user']

class AuctionSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    winner = serializers.StringRelatedField(read_only=True)
    active_bidder = serializers.StringRelatedField(read_only=True)
    seller_name = serializers.CharField(source='car.user.username', read_only=True)


    class Meta:
        model = Auction
        fields = ('id', 'car', 'price', 'end_time', 'winner', 'active_bidder', 'seller_name')



class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'user', 'auction', 'price', 'created_at']
        read_only_fields = ['id', 'user', 'auction', 'created_at']


class BidAllSerializer(serializers.ModelSerializer):
    car_name = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['id', 'user', 'auction', 'car_name', 'price', 'created_at']
        read_only_fields = ['id', 'user', 'auction', 'created_at']

    def get_car_name(self, obj):
        return obj.auction.car.name
    
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'auction', 'status']

