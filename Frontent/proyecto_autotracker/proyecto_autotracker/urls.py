"""
URL configuration for proyecto_autotracker project.

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
from proyecto_autotracker.views import Registro_persona
from proyecto_autotracker.views import consulta
from proyecto_autotracker.views import Datos_de_auto
from proyecto_autotracker.views import login
from proyecto_autotracker.views import monitoreo
from proyecto_autotracker.views import consulta_tracking
from proyecto_autotracker.views import Registros_usuarios
from proyecto_autotracker.views import Registros_robo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Registro_persona/', Registro_persona),
    path('consulta/', consulta),
    path('Datos_de_auto/', Datos_de_auto),
    path('login/', login),
    path('monitoreo/', monitoreo),
    path('Registros_usuarios/', Registros_usuarios),
    path('tracking/', consulta_tracking),
    path('Registro_persona/', Registro_persona),
    path('Registros_del_Robo/', Registros_robo),

]
