from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from applications.views import DadosColetaViewSet, DadosRetreinoViewSet, DadosPredicaoViewSet, DadosEstatisticaViewSet, Dashboard
from . import dashboard

router = routers.DefaultRouter()
router.register(r'dadoscoleta', DadosColetaViewSet, basename='dadoscoleta')
router.register(r'dadosretreino', DadosRetreinoViewSet, basename='dadosretreino')
router.register(r'dadospredicao', DadosPredicaoViewSet, basename='dadospredicao')
router.register(r'dadosestatistica', DadosEstatisticaViewSet, basename='dadosestatistica')


urlpatterns = [
    path('services/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('services-auth/', include('rest_framework.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('dash/', Dashboard.as_view())
]
