from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from applications.views import coletaViewSet, estatisticaViewSet, predicaoViewSet, Dashboard
from . import dashboard

router = routers.DefaultRouter()
router.register(r'coleta', coletaViewSet, basename='coleta')
router.register(r'predicao', predicaoViewSet, basename='predicao')
router.register(r'estatistica', estatisticaViewSet, basename='estatistica')


urlpatterns = [
    path('services/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('services-auth/', include('rest_framework.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('dash/', Dashboard.as_view())
]
