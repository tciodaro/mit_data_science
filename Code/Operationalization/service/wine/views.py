from django.shortcuts import render
from rest_framework import viewsets

from wine.models import *
from wine.serializers import *

# Create your views here.


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows supplier to be viewed or edited.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer



class SupplierMenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    """
    queryset = SupplierMenu.objects.all()
    serializer_class = SupplierMenuSerializer




class EstimateScoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wine to be viewed or edited.
    """
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
