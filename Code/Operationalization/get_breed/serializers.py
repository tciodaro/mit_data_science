from rest_framework import serializers
from get_breed.models import Pictures

from django.db import models

class PicturesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pictures
        fields = ['address','real_breed','classification', 'estimated_score1', 'estimated_score2', 'estimated_score3']
