from django.contrib import admin
from .models import Appointment, Car, Auction, Bid

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'price', 'end_time', 'winner')
    list_filter = ('car', 'end_time')
    search_fields = ('car__name', 'car__model')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'auction', 'car_name', 'price', 'created_at')
    list_filter = ('user', 'auction')
    search_fields = ('user__username', 'auction__car__name', 'auction__car__model')

    def car_name(self, obj):
        return obj.auction.car.name

    car_name.short_description = 'Car Name'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'auction', 'status')
    list_filter = ('auction', 'status')
    search_fields = ('auction__car__name', 'auction__car__model')

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Car)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)