from rest_framework import serializers
from .models import  DadosColeta, DadosRetreino, DadosPredicao, DadosEstatistica
from datetime import date

# Serializers define the API representation.

# Serializa os dados di banco de dados em json que será retornado pela API


class DadosColetaSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = DadosColeta        
        fields = ['id','din_evento','dsc_manutencao','tip_evento']


class DadosRetreinoSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = DadosRetreino        
        fields = ['id_sin','dsc_texto','tip_supervisao','din_execucao','tip_evento','tip_predicao','pct_predicao']        


class DadosPredicaoSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = DadosPredicao        
        fields = ['id_sin','dsc_texto','tip_supervisao','din_execucao','tip_evento','tip_predicao','pct_predicao']     


class DadosEstatisticaSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = DadosEstatistica        
        fields = ['din_execucao','dsc_predicao','qtd_registro']     


        