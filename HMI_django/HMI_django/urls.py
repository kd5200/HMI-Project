"""
URL configuration for HMI_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from HMIapp.views import *

from rest_framework.routers import DefaultRouter

from HMIapp.viewset1 import ModelViewSet

router = DefaultRouter()
router.register(r'weather', ModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ReactView.as_view(), name="anything"),
    path('cities/', get_cities_from_google_sheet, name='get_cities'),
    path('sheets/', get_google_sheets_data, name='get_data'),
    path('weathercon/<str:cityName>/', get_weather_info, name='get_condition'),
    path('cities_states_by_weather/', get_cities_states_by_weather, name='get_cities_states_by_weather'),





]

urlpatterns += router.urls
