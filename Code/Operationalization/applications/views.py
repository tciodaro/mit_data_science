from django.shortcuts import render
from rest_framework import viewsets
from .models import  coleta, predicao, estatistica
from .serializers import coletaSerializer, predicaoSerializer, estatisticaSerializer
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class coletaViewSet(viewsets.ModelViewSet):
    
    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['id','din_evento']
    ordering_fields = ['din_evento','id']
    
    # Ordenação default
    ordering = ['din_evento','id']

    serializer_class = coletaSerializer

    def get_queryset(self):
                 
        param_dat_inicio = self.request.query_params.get('dat_inicio', None)
        param_dat_fim = self.request.query_params.get('dat_fim', None)
        
        #import pdb; pdb.set_trace(); 
        
        if param_dat_inicio is not None and param_dat_fim is not None:
            # Converte parâmetros de entrada em datas. Aguarda dd/mm/aaaa
            dat_inicio = datetime.strptime(param_dat_inicio, '%d/%m/%Y')
            dat_fim = datetime.strptime(param_dat_fim, '%d/%m/%Y')

            #Filtrar o dia ou intervalo
            if dat_inicio == dat_fim:
                result = coleta.objects.filter(din_evento=dat_inicio)
            else:
                result = coleta.objects.filter(din_evento__gte=dat_inicio,din_evento__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = coleta.objects.all()
        return result


class estatisticaViewSet(viewsets.ModelViewSet):
    
    serializer_class = estatisticaSerializer

    def get_queryset(self):
        estatistica.objects.all()
        result = estatistica.objects.all()
        return result
        


class predicaoViewSet(viewsets.ModelViewSet):
    
    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['id','din_execucao']
    ordering_fields = ['din_execucao','id']
    
    # Ordenação default
    ordering = ['din_execucao','id']

    serializer_class = predicaoSerializer

    def get_queryset(self):
                 
        param_dat_inicio = self.request.query_params.get('dat_inicio', None)
        param_dat_fim = self.request.query_params.get('dat_fim', None)
        
        #import pdb; pdb.set_trace(); 
        
        if param_dat_inicio is not None and param_dat_fim is not None:
            # Converte parâmetros de entrada em datas. Aguarda dd/mm/aaaa
            dat_inicio = datetime.strptime(param_dat_inicio, '%d/%m/%Y')
            dat_fim = datetime.strptime(param_dat_fim, '%d/%m/%Y')

            #Filtrar o dia ou intervalo
            if dat_inicio == dat_fim:
                result = predicao.objects.filter(din_execucao=dat_inicio)
            else:
                result = predicao.objects.filter(din_execucao__gte=dat_inicio,din_execucao__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = predicao.objects.all()
        return result




class Dashboard(APIView):
       
    def get(self, request):
       return render(request, 'dashboard.html')