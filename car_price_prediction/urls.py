from django.urls import path
from .views import CarPricePrediction, train_model


urlpatterns = [
    path('train_model/', train_model, name='train_model'),
    path('predict_price/', CarPricePrediction.as_view(), name='predict_price')
]