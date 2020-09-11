
from rest_framework import serializers
from forecast.models import *

from django.db import models

# Create your models here.

class MeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurements
        fields = ['date','PJME_MW']


class ForecastModelsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ForecastModels
        fields = ['name','train_initial_date','train_last_date','test_score','status']



class ForecastsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Forecasts
        fields = ['PJME_MW','date', 'error',  'percentage_error', 'forecast_model', 'measurement']
