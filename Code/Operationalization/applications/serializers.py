from rest_framework import serializers
from .models import  coleta, treinoteste, predicao, estatistica
from datetime import date

# Serializers define the API representation.

# Serializa os dados di banco de dados em json que será retornado pela coletaAPI

class coletaSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = coleta        
        fields = ['id','din_evento','dsc_texto']

class treinotesteSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = treinoteste        
        fields = ['id','dsc_texto','tip_legenda','tip_predicao','pct_predicao','din_calculo']

class predicaoSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = predicao        
        fields = ['id','dsc_texto','tip_supervisao','din_execucao','tip_predicao','pct_predicao','val_realpredicao']


class estatisticaSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = estatistica        
        fields = ['id','din_execucao','dsc_predicao','qtd_registro']


