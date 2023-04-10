from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max


class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField()
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive'), ('cancelled', 'Cancelled'), ('completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return self.name

  
class Auction(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='auctions')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.DateTimeField(default=timezone.now)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')

    def save(self, *args, **kwargs):
        print('Saving auction...')
        print('End time:', self.end_time)
        max_bid = Bid.objects.filter(auction=self).aggregate(Max('price'))
        print('Max bid:', max_bid)
        super().save(*args, **kwargs)
        print('Current time:', timezone.now())
        print(self.winner)
        if self.end_time <= timezone.now() and not self.winner:
            print('Updating winner...')
            if max_bid['price__max']:
                winning_bid = Bid.objects.filter(auction=self, price=max_bid['price__max']).first()
                print(winning_bid)
                print(winning_bid.user)
                self.winner = winning_bid.user
                self.save(update_fields=['winner'])
                

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.auction} - {self.price}"
    
class Appointment(models.Model):
    date = models.DateField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive')