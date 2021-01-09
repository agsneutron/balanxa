# coding=utf-8
from django.conf.urls import url

from Proceso.api import *


app_name = 'Proceso'

urlpatterns = [
     #/Procesa/

     url(r'^get_keys/$', ProcesaArchivo.as_view(), name='procesar'),

]