"""covid19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import  url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, path
from rest_framework import routers
from forecast import views

router = routers.DefaultRouter()
router.register(r'countries', views.CountriesViewSet)
router.register(r'measurements', views.MeasurementsViewSet)
router.register(r'forecast_models', views.ForecastModelsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^update_models/', views.UpdateModels.as_view()),
    url(r'^forecast_country/', views.ForecastCountry.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
