from django.db import models

class ai(models.Model):
    car_name = models.CharField(max_length=100)
    year = models.IntegerField()
    kms_driven = models.IntegerField()
    fuel_type = models.CharField(max_length=10)
    selling_price = models.FloatField()