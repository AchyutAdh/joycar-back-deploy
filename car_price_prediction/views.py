# car_price_prediction/views.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarPricePredictionSerializer
import os

from car_price_prediction import serializers

def train_model(request):
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'car_data.csv')

    # Using double backslashes
    car_dataset = pd.read_csv(data_path)

    # Encode categorical variables
    car_dataset.replace({'Fuel_Type':{'Petrol':0,'Diesel':1,'CNG':2}},inplace=True)
    car_dataset.replace({'Seller_Type':{'Dealer':0,'Individual':1}},inplace=True)
    car_dataset.replace({'Transmission':{'Manual':0,'Automatic':1}},inplace=True)

    # Split the dataset into training and testing sets
    X = car_dataset.drop(['Car_Name', 'Selling_Price'],axis=1)
    Y = car_dataset['Selling_Price']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state=2)

    # Train a Linear Regression model on the training set
    lin_reg_model = LinearRegression()
    lin_reg_model.fit(X_train,Y_train)

    # Save the trained model to a .pkl file
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
    joblib.dump(lin_reg_model, model_path)

    # Return a response indicating that the model has been trained and saved
    return JsonResponse({'message': 'Model trained and saved successfully'})


class CarPricePrediction(APIView):
    def post(self, request):
        # Load the trained model from the .pkl file
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
        model = joblib.load(model_path)

        # Validate the input data using the serializer
        serializer = CarPricePredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Add missing features to the car data dictionary
        car_data = {
            'Year': validated_data['year'],
            'Present_Price': validated_data.get('present_price', 0),
            'Kms_Driven': validated_data['kms_driven'],
            'Fuel_Type': validated_data['fuel_type'],
            'Seller_Type': validated_data.get('seller_type', 'Dealer'),
            'Transmission': validated_data.get('transmission', 'Manual'),
            'Owner': validated_data.get('owner', 0),
        }

        # Encode the car data using the same encoding used for Fuel_Type
        car_data_encoded = pd.DataFrame(car_data, index=[0])
        car_data_encoded.replace({
            'Fuel_Type': {'Petrol': 0, 'Diesel': 1, 'CNG': 2},
            'Seller_Type': {'Dealer': 0, 'Individual': 1},
            'Transmission': {'Manual': 0, 'Automatic': 1}
        }, inplace=True)

        # Load the car data from the database

        # Make a prediction using the trained model
        prediction = model.predict(car_data_encoded)
        predicted_price = round(prediction[0], 2)

        return Response({'selling_price': predicted_price}, status=status.HTTP_200_OK)