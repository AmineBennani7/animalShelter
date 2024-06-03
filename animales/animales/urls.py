"""
URL configuration for animales project.

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
from django.urls import path
from main import views as main_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.index, name='index'),
    path('index/', main_views.index, name='index'),
    path('listar_todo/', main_views.listar_todo, name='listar_todo'),
    path('buscar_nombre_raza/', main_views.buscar_nombre_raza, name='buscar_nombre_raza'),
    path('buscar_genero/', main_views.buscar_genero, name='buscar_genero'),
    path('buscar_tipo/', main_views.buscar_tipo, name='buscar_tipo'),
    path('buscar_tamano/', main_views.buscar_tamano, name='buscar_tamano'),
    path('buscar_tipo_tamano/', main_views.buscar_tipo_tamano, name='buscar_tipo_tamano'),
    path('buscar_rango_edades/', main_views.buscar_rango_edades, name='buscar_rango_edades'),
    path('buscar_avanzado/', main_views.buscar_avanzado, name='buscar_avanzado'),
]


