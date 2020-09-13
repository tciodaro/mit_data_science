from rest_framework import serializers
from .models import  DadosColeta, DadosRetreino, DadosPredicao, DadosEstatistica
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
        fields = ['id','dsc_texto','tip_supervisao','din_execucao','tip_legenda','tip_predicao','pct_predicao']


class estatisticaSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = estatistica        
        fields = ['id','din_execucao','dsc_predicao','qtd_registro']





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


        