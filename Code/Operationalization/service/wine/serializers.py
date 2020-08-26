from rest_framework import serializers
from wine import models


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Supplier
        fields = ['name','address','created']


class WineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Wine
        fields = ['name','fixed_acidity','volatile_acidity','citric_acid',
                  'residual_sugar','chlorides','free_sulfur_dioxide',
                  'total_sulfur_dioxide','density','pH','sulphates',
                  'alcohol','estimated_score']

class SupplierMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupplierMenu
        fields = ['supplier','wine','created']


# END OF FILE
