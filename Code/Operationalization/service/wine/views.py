from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wine.models import *
from wine.serializers import *
from wine import dashboard

# Create your views here.


def dashboard_home(requests):
    dashboard.update_dash()
    return render(requests, 'wine/welcome.html')


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows supplier to be viewed or edited.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer



class SupplierMenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows menu to be viewed or edited.
    """
    queryset = SupplierMenu.objects.all()
    serializer_class = SupplierMenuSerializer


class WineAPIView(APIView):
    """
    API endpoint that allows wines to be viewed or edited.
    """
    def get(self, request):
        serializer = WineSerializer(Wine.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        data = dict([(k,v[0] if isinstance(v, list) else v)
                     for k,v in request.data.items()
                     if k != 'supplier'])
        wine, created = Wine.objects.get_or_create(**data)
        if created:
            wine.save_estimate()

        serializer = WineSerializer(wine, many=False)

        # Associate wine and supplier
        supplier, created = Supplier.objects.get_or_create(name=request.data['supplier'])
        menu, created = SupplierMenu.objects.get_or_create(supplier=supplier, wine=wine)

        return Response(serializer.data, status=status.HTTP_200_OK)



# END OF FILE
