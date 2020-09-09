from django.shortcuts import render
from rest_framework import viewsets
from .models import DadosColeta, DadosRetreino , DadosPredicao, DadosEstatistica
from .serializers import DadosColetaSerializer,DadosRetreinoSerializer , DadosPredicaoSerializer, DadosEstatisticaSerializer
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# ViewSets define the view behavior.
class DadosColetaViewSet(viewsets.ModelViewSet):

    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['id','din_evento','dsc_manutencao']
    ordering_fields = ['din_evento','id']
    
    # Ordenação default
    ordering = ['-din_evento','id']

    serializer_class = DadosColetaSerializer

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
                result = DadosColeta.objects.filter(din_evento=dat_inicio)
            else:
                result = DadosColeta.objects.filter(din_evento__gte=dat_inicio,din_evento__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = DadosColeta.objects.all()
        return result


# ViewSets define the view behavior.
class DadosRetreinoViewSet(viewsets.ModelViewSet):

    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['id_sin','tip_supervisao','din_execucao','tip_evento','tip_predicao']
    ordering_fields = ['din_execucao']
    
    # Ordenação default
    ordering = ['din_execucao']

    serializer_class = DadosRetreinoSerializer

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
                result = DadosRetreino.objects.filter(din_execucao=dat_inicio)
            else:
                result = DadosRetreino.objects.filter(din_execucao__gte=dat_inicio,din_execucao__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = DadosRetreino.objects.all()
        return result


#ViewSets define the view behavior.
class DadosPredicaoViewSet(viewsets.ModelViewSet):

    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['din_execucao']
    ordering_fields = ['din_execucao']
    
    # Ordenação default
    ordering = ['din_execucao']

    serializer_class = DadosPredicaoSerializer

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
                result = DadosPredicao.objects.filter(din_execucao=dat_inicio)
            else:
                result = DadosPredicao.objects.filter(din_execucao__gte=dat_inicio,din_execucao__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = DadosPredicao.objects.all()
        return result        


#ViewSets define the view behavior.
class DadosEstatisticaViewSet(viewsets.ModelViewSet):

    #Ativa filtro de backend, busca genêrica e ordenação para as informações abaixo. obs: por filtro direto busca exata, por search busca tipo 'like'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = search_fields = ['din_execucao']
    ordering_fields = ['din_execucao']
    
    # Ordenação default
    ordering = ['din_execucao']

    serializer_class = DadosEstatisticaSerializer

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
                result = DadosEstatistica.objects.filter(din_execucao=dat_inicio)
            else:
                result = DadosEstatistica.objects.filter(din_execucao__gte=dat_inicio,din_execucao__lte=dat_fim)

        else:
            # Retorna todos os resultados caso não sejam passados parâmetros
            result = DadosEstatistica.objects.all()
        return result        


class Dashboard(APIView):
       
    def get(self, request):
       return render(request, 'dashboard.html')