from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns =[
	path('',login_required(views.index), name='index'),
	path('authsat',views.authSat, name='authsat'),
	path('solicitudes',views.solicitudesRFC, name='solicitudesrfc'),
	path('verifica',views.verificaSolicitud, name='verificasolicitud'),
	path('zip',views.downloadFileSat, name='downloadfileSat'),
	path('readxml',views.readXML, name='readxml'),
	path('add/poliza',views.solicitudPoliza, name='solicitudpoliza'),
	path('details/poliza',views.detailsPoliza, name='detailspoliza'),
	path('search/poliza',views.searchPoliza,name='searchpoliza'),
	path('remove/cfdisource',views.removeItemCfdi,name='removeitemcfdi'),
	path('search/template',views.templatesbyUser,name='templatesbyuser'),
]