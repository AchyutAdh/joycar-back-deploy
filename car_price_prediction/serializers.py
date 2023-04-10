from rest_framework import serializers
import pandas as pd
import os

# class CarPricePredictionSerializer(serializers.Serializer):
#     car_name = serializers.CharField(max_length=100)
#     year = serializers.IntegerField()
#     kms_driven = serializers.IntegerField()
#     fuel_type = serializers.ChoiceField(choices=['Petrol', 'Diesel', 'CNG'])

#     def validate(self, data):
#         csv_path = os.path.join(os.path.dirname(__file__), 'data', 'car_data.csv')
#         # Check if the car data is valid
#         car_dataset = pd.read_csv(csv_path)
#         car_data = car_dataset[(car_dataset['Car_Name'] == data['car_name']) & (car_dataset['Year'] == data['year']) & (car_dataset['Kms_Driven'] == data['kms_driven']) & (car_dataset['Fuel_Type'] == data['fuel_type'])]
#         if len(car_dataset) == 0:
#             raise serializers.ValidationError('Car data not found')
#         return data
    
    

class CarPricePredictionSerializer(serializers.Serializer):
    car_name = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    kms_driven = serializers.IntegerField()
    fuel_type = serializers.ChoiceField(choices=['Petrol', 'Diesel', 'CNG'])

    def validate(self, data):
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'car_data.csv')
        # Check if the car data is valid
        car_dataset = pd.read_csv(csv_path)
        if len(car_dataset) == 0:
            raise serializers.ValidationError('Car data not found')
        return data