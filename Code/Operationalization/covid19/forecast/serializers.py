
from rest_framework import serializers
from forecast.models import *

from django.db import models

# Create your models here.

class CountriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Countries
        fields = ['code',]


class MeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurements
        fields = ['date','cases','recovered', 'country']


class ForecastModelsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ForecastModels
        fields = ['name','train_last_date', 'country', 'test_score','status']



class ForecastsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forecasts
        fields = ['estimated_cases','date', 'error', 'forecast_model',]
