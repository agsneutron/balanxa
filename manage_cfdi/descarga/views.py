from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from django.http import JsonResponse
import json
from django.core import serializers
from django.db import connections
import hashlib
import sys
from django.views.decorators.csrf import csrf_exempt
import os
from django.core.files import File
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from descarga.message import *
from descarga.querys import *
from descarga.utils import *
from descarga.urlssat import *
import datetime
from xml.dom import minidom
from xml.dom.minidom import Node
from xml.dom.minidom import parseString

def index(request):

	return render(request, 'index.html')

@csrf_exempt
def authSat(request):
	data = []
	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'rfc' not in request.GET or 'startdate' not in request.GET or 'enddate' not in request.GET or 'cfdi_solicitud_tipo' not in request.GET or 'cfdi_solicitud_pdf' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		querysolicitudxRFC = getinfoFromTb('api_tb_users_rfc','user_rfc',request.GET['rfc'],'user_rfc')
		
		if querysolicitudxRFC  is None:
			data = codemessage(404)
			return JsonResponse(data,safe=False)
			sys.exit();
		else:
			"""
			"""
	startdate = request.GET['startdate']
	enddate = request.GET['enddate']
	startdate = startdate.split("-")
	enddate = enddate.split("-")
	try:
		startdateY=int(startdate[0])
		startdateM=int(startdate[1])
		startdateD=int(startdate[2])
		enddateY=int(enddate[0])
		enddateM=int(enddate[1])
		enddateD=int(enddate[2])
	except:
		data = codemessage(404)
		return JsonResponse(data,safe=False)
		sys.exit();

	cerLocation = getinfoFromTb('api_tb_users_rfc','user_rfc',request.GET['rfc'],'user_rfc_location_cer')[0]
	keyLocation = getinfoFromTb('api_tb_users_rfc','user_rfc',request.GET['rfc'],'user_rfc_location_key')[0]

	user_rfc = getinfoFromTb('api_tb_users_rfc','user_rfc',request.GET['rfc'],'user_rfc')[0]
	secretPassword = getinfoFromTb('api_tb_users_rfc','user_rfc',request.GET['rfc'],'user_rfc_clave')[0]


	dateCreated = datetime.datetime(startdateY,startdateM,startdateD)
	dateExpires = datetime.datetime(enddateY,enddateM,enddateD)

	cfdi_solicitud_rango = str(dateCreated.strftime("%Y-%m-%d") + " - " + dateExpires.strftime("%Y-%m-%d"))
	try:
		fielg = fiel(request,cerLocation,keyLocation,secretPassword)
		pass
	except:
		data = codemessage(907)
		return JsonResponse(data,safe=False)
		sys.exit();

	cfdi_token_response = getToken(request,user_rfc,fielg)
	if cfdi_token_response == None:
		data = codemessage(908)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass
	listaddtokenResponse = guardaToken(request,user_rfc,cfdi_token_response)
	cfdi_token_id = listaddtokenResponse["cfdi_token_id"]

	requestDonwload = requestDownload(request,user_rfc,cfdi_token_response,dateCreated,dateExpires,fielg,"CFDI")
	idResultEmitidos = requestDonwload["solicitudDescargaEmitidos"]["id_solicitud"]
	codResultEmitidos = requestDonwload["solicitudDescargaEmitidos"]["cod_estatus"] 
	mensajeResultEmitidos = requestDonwload["solicitudDescargaEmitidos"]["mensaje"]
	idResultsRecibidos = requestDonwload["solicitudDescargaRecibidos"]["id_solicitud"]
	codResultsRecibidos = requestDonwload["solicitudDescargaRecibidos"]["cod_estatus"]
	mensajeResultsRecibidos = requestDonwload["solicitudDescargaRecibidos"]["mensaje"]

	cfdi_solicitud_pdf = request.GET['cfdi_solicitud_pdf']
	#Guardando Solicitud
	if request.GET['cfdi_solicitud_tipo'] == 'Todas':
		listaddsolicitudEmitidos = guardaSolicitud(request,idResultEmitidos,codResultEmitidos,mensajeResultEmitidos,cfdi_token_id,"Emitidos",user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf)
		listaddsolicitudRecibidos = guardaSolicitud(request,idResultsRecibidos,codResultsRecibidos,mensajeResultsRecibidos,cfdi_token_id,"Recibidos",user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf)
		cfdi_solicitud_id_e = listaddsolicitudEmitidos["cfdi_solicitud_id"]
		cfdi_solicitud_id_r = listaddsolicitudRecibidos["cfdi_solicitud_id"]
	elif request.GET['cfdi_solicitud_tipo'] == 'Emitidos':
		listaddsolicitudEmitidos = guardaSolicitud(request,idResultEmitidos,codResultEmitidos,mensajeResultEmitidos,cfdi_token_id,"Emitidos",user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf)
		listaddsolicitudRecibidos = None
		cfdi_solicitud_id_e = listaddsolicitudEmitidos["cfdi_solicitud_id"]
		cfdi_solicitud_id_r = None
	elif request.GET['cfdi_solicitud_tipo'] == 'Recibidos':
		listaddsolicitudRecibidos = guardaSolicitud(request,idResultsRecibidos,codResultsRecibidos,mensajeResultsRecibidos,cfdi_token_id,"Recibidos",user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf)
		listaddsolicitudEmitidos = None
		cfdi_solicitud_id_e = None
		cfdi_solicitud_id_r = listaddsolicitudRecibidos["cfdi_solicitud_id"]


	print ("cfdi_token_response: " + cfdi_token_response)
	print ("user_rfc: " + user_rfc)
	print ("idResultEmitidos: " + idResultEmitidos)
	print ("idResultsRecibidos: " + idResultsRecibidos)
	print ("fielg: " + str(fielg))

	verifyRequestDonwload = verifyDownload(request,cfdi_token_response,user_rfc,idResultEmitidos,idResultsRecibidos,fielg)
	print ("verifyDownload: " + str(verifyRequestDonwload))
	vsdecod_estatus = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['cod_estatus']
	vsdeestado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['estado_solicitud']
	vsdecodigo_estado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['codigo_estado_solicitud']
	vsdenumero_cfdis = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['numero_cfdis']
	vsdemensaje = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['mensaje']
	try:
		if len(verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['paquetes']) > 0:
			vsdepaquetes = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['paquetes'][0]
		else:
			vsdepaquetes = ""
	except:
		vsdepaquetes = ""
	vsdrcod_estatus = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['cod_estatus']
	vsdrestado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['estado_solicitud']
	vsdrcodigo_estado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['codigo_estado_solicitud']
	vsdrnumero_cfdis = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['numero_cfdis']
	vsdrmensaje = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['mensaje']
	try:
		if len(verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['paquetes']) > 0:
			vsdrpaquetes = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['paquetes'][0]
		else:
			vsdrpaquetes = ""
	except:
		vsdrpaquetes = ""
	listaddverificacionEmitidos = guardaVerificacion(request,vsdecod_estatus,vsdecod_estatus,vsdecodigo_estado_solicitud,vsdenumero_cfdis,vsdemensaje,cfdi_solicitud_id_e,cfdi_token_id,"Emitidos",user_rfc,satEstado(vsdeestado_solicitud))
	listaddverificacionRecibidos = guardaVerificacion(request,vsdrcod_estatus,vsdrcod_estatus,vsdrcodigo_estado_solicitud,vsdrnumero_cfdis,vsdrmensaje,cfdi_solicitud_id_r,cfdi_token_id,"Recibidos",user_rfc,satEstado(vsdrestado_solicitud))
	#Guardando Verificacion
	if request.GET['cfdi_solicitud_tipo'] == 'Todas':
		listaddverificacionEmitidos = guardaVerificacion(request,vsdecod_estatus,vsdecod_estatus,vsdecodigo_estado_solicitud,vsdenumero_cfdis,vsdemensaje,cfdi_solicitud_id_e,cfdi_token_id,"Emitidos",user_rfc,satEstado(vsdeestado_solicitud))
		listaddverificacionRecibidos = guardaVerificacion(request,vsdrcod_estatus,vsdrcod_estatus,vsdrcodigo_estado_solicitud,vsdrnumero_cfdis,vsdrmensaje,cfdi_solicitud_id_r,cfdi_token_id,"Recibidos",user_rfc,satEstado(vsdrestado_solicitud))
	elif request.GET['cfdi_solicitud_tipo'] == 'Emitidos':
		listaddverificacionEmitidos = guardaVerificacion(request,vsdecod_estatus,vsdecod_estatus,vsdecodigo_estado_solicitud,vsdenumero_cfdis,vsdemensaje,cfdi_solicitud_id_e,cfdi_token_id,"Emitidos",user_rfc,satEstado(vsdeestado_solicitud))
		listaddverificacionRecibidos = None
	elif request.GET['cfdi_solicitud_tipo'] == 'Recibidos':
		listaddverificacionRecibidos = guardaVerificacion(request,vsdrcod_estatus,vsdrcod_estatus,vsdrcodigo_estado_solicitud,vsdrnumero_cfdis,vsdrmensaje,cfdi_solicitud_id_r,cfdi_token_id,"Recibidos",user_rfc,satEstado(vsdrestado_solicitud))
		listaddverificacionEmitidos = None

	if vsdeestado_solicitud == "3" and vsdrestado_solicitud == "3":
		#Datos de paquetes
		path_location_paquetes = "/home/storage/files/"

		getRequestDownload = getDownload(request,cfdi_token_response,user_rfc,vsdepaquetes,vsdrpaquetes,fielg)
		dpecod_estatus = getRequestDownload['descargaEmitidos']['cod_estatus']
		dpemensaje = getRequestDownload['descargaEmitidos']['mensaje']
		dpepaquete_b64 = getRequestDownload['descargaEmitidos']['paquete_b64']
		cfdi_paquete_location_e_uuid = genUuidv4(request)
		cfdi_paquete_location_e_name = "Emitidos" + "-" + user_rfc + "-" + cfdi_paquete_location_e_uuid + ".zip"
		cfdi_paquete_location_e_dir = path_location_paquetes + cfdi_paquete_location_e_uuid + "/"
		cfdi_paquete_location_e = b64toZip(request,dpepaquete_b64,cfdi_paquete_location_e_name,cfdi_paquete_location_e_dir)
		cfdi_paquete_location_e_files = "No existen archivos dentro de la respuesta"
		if cfdi_paquete_location_e != None:
			cfdi_paquete_location_e_files = extractZip(request,cfdi_paquete_location_e_dir+cfdi_paquete_location_e_name,cfdi_paquete_location_e_dir,"")
			pass

		dprcod_estatus = getRequestDownload['descargaRecibidos']['cod_estatus']
		dprmensaje = getRequestDownload['descargaRecibidos']['mensaje']
		dprpaquete_b64 = getRequestDownload['descargaRecibidos']['paquete_b64']
		cfdi_paquete_location_r_uuid = genUuidv4(request)
		cfdi_paquete_location_r_name = "Recibidos" + "-" + user_rfc + "-" + cfdi_paquete_location_r_uuid + ".zip"
		cfdi_paquete_location_r_dir = path_location_paquetes + cfdi_paquete_location_r_uuid + "/"
		cfdi_paquete_location_r = b64toZip(request,dprpaquete_b64,cfdi_paquete_location_r_name,cfdi_paquete_location_r_dir)
		cfdi_paquete_location_r_files = "No existen archivos dentro de la respuesta"
		if cfdi_paquete_location_r != None:
			cfdi_paquete_location_r_files = extractZip(request,cfdi_paquete_location_r_dir+cfdi_paquete_location_r_name,cfdi_paquete_location_r_dir,"")
			pass

		listaddpaquetesEmitidos = solicitudPaquetes(request,dpecod_estatus,dpemensaje,dpepaquete_b64,cfdi_paquete_location_e,cfdi_solicitud_id_e,cfdi_token_id,user_rfc,'Emitidos',cfdi_paquete_location_e_files)
		listaddpaquetesRecibidos = solicitudPaquetes(request,dprcod_estatus,dprmensaje,dprpaquete_b64,cfdi_paquete_location_r,cfdi_solicitud_id_r,cfdi_token_id,user_rfc,'Recibidos',cfdi_paquete_location_r_files)
		#Datos de paquetes
	else:
		listaddpaquetesEmitidos = "La solicitud que intentas descargar no esta disponible"
		listaddpaquetesRecibidos = "La solicitud que intentas descargar no esta disponible"
	data = {
		'query':[{'sucess':True,'user_rfc':user_rfc,'dateCreated':dateCreated,'dateExpires':dateExpires}],
		'token':[],
		'solicitud':[],
		'verificacion':[],
		'paquetes':[],
		'sessionData':[]
	}
	#querysessionData = sendLog(user_rfc,'user_rfc',request,'obtenersolicitud')
	#data['sessionData'].append(querysessionData)
	data['token'].append(listaddtokenResponse)
	data['solicitud'].append(listaddsolicitudEmitidos)
	data['solicitud'].append(listaddsolicitudRecibidos)
	data['verificacion'].append(listaddverificacionEmitidos)
	data['verificacion'].append(listaddverificacionRecibidos)
	data['paquetes'].append(listaddpaquetesEmitidos)
	data['paquetes'].append(listaddpaquetesRecibidos)


	response = JsonResponse(data,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def solicitudesRFC(request):
	data = []
	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'rfc' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		querysolicitudxRFC = solicitudesporRFC(request,request.GET['rfc'])
		if querysolicitudxRFC  is None:
			data = codemessage(404)
			return JsonResponse(data,safe=False)
			sys.exit();
		else:
			"""
			"""

	data = {
		'solicitudes':[],
		'sessionData':[]
	}
	#querysessionData = sendLog(request.GET['rfc'],'rfc',request,'solicitalistarfc')
	#data['sessionData'].append(querysessionData)
	data['solicitudes'].append(querysolicitudxRFC)

	response = JsonResponse(data,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def verificaSolicitud(request):
	zip_download = "No disponible"
	dir_location = "No disponible"
	data = []
	listaddpaquetessat = []
	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'cfdi_solicitud_id' not in request.GET or 'cfdi_solicitud_sat_id' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		querysolicitudxEstado = getinfoFromTb('cfdi_solicitud','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_solicitud_mensaje')
		if querysolicitudxEstado  is None:
			data = codemessage(404)
			return JsonResponse(data,safe=False)
			sys.exit();
		else:
			"""
			"""	
			cfdi_solicitud_tipo = getinfoFromTb('cfdi_solicitud','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_solicitud_tipo')
			user_rfc = getinfoFromTb('cfdi_solicitud','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'user_rfc')

			cerLocation = getinfoFromTb('api_tb_users_rfc','user_rfc',user_rfc,'user_rfc_location_cer')[0]
			keyLocation = getinfoFromTb('api_tb_users_rfc','user_rfc',user_rfc,'user_rfc_location_key')[0]
			secretPassword = getinfoFromTb('api_tb_users_rfc','user_rfc',user_rfc,'user_rfc_clave')[0]
			try:
				fielg = fiel(request,cerLocation,keyLocation,secretPassword)
				pass
			except:
				data = codemessage(907)
				return JsonResponse(data,safe=False)
				sys.exit();

			cfdi_token_response = getToken(request,user_rfc,fielg)
			listaddtokenResponse = guardaToken(request,user_rfc,cfdi_token_response)
			cfdi_token_id = listaddtokenResponse["cfdi_token_id"]

	cfdi_verificacion_id = getinfoFromTb('cfdi_verificacion','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_verificacion_id')
	cfdi_verificacion_estado_solicitud = getinfoFromTb('cfdi_verificacion','cfdi_verificacion_id',cfdi_verificacion_id,'cfdi_verificacion_estado_solicitud')
	if "3" not in cfdi_verificacion_estado_solicitud[0]:
		satestado_solicitud = ""
		verificacionsatRequestStatus = ""	
		if cfdi_solicitud_tipo[0] == "Recibidos":
			verifyRequestDonwload = verifyDownloadR(request,cfdi_token_response,user_rfc,request.GET['cfdi_solicitud_sat_id'],fielg)
			satcod_estatus = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['cod_estatus']
			satestado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['estado_solicitud']
			satcodigo_estado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['codigo_estado_solicitud']
			satnumero_cfdis = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['numero_cfdis']
			satmensaje = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['mensaje']
			try:
				if len(verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['paquetes']) > 0:
					satpaquetes = verifyRequestDonwload['verificacionSolicitudDescargaRecibidos']['paquetes']
				else:
					satpaquetes = ""
			except:
				vsdrpaquetes = ""
			
		
		elif cfdi_solicitud_tipo[0] == "Emitidos":
			verifyRequestDonwload = verifyDownloadE(request,cfdi_token_response,user_rfc,request.GET['cfdi_solicitud_sat_id'],fielg)
			satcod_estatus = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['cod_estatus']
			satestado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['estado_solicitud']
			satcodigo_estado_solicitud = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['codigo_estado_solicitud']
			satnumero_cfdis = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['numero_cfdis']
			satmensaje = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['mensaje']
			try:
				if len(verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['paquetes']) > 0:
					satpaquetes = verifyRequestDonwload['verificacionSolicitudDescargaEmitidos']['paquetes']
				else:
					satpaquetes = ""
			except:
				vsdepaquetes = ""
		resultQueryUpdateVerificacion = QueryverificacionsatRequestStatus = actualizaVerificacion(satcod_estatus,satmensaje,satEstado(satestado_solicitud),satcodigo_estado_solicitud,satnumero_cfdis,satpaquetes,cfdi_verificacion_id)
		verificacionsatRequestStatus = {'cfdi_verificacion_id':cfdi_verificacion_id,'cfdi_verificacion_cod_estatus':satcod_estatus,'cfdi_verificacion_mensaje':satmensaje,'cfdi_verificacion_estado_solicitud':satEstado(satestado_solicitud),'cfdi_verificacion_cod_estado_solicitud':satcodigo_estado_solicitud,'cfdi_verificacion_numero_cfdi':satnumero_cfdis,'cfdi_verificacion_paquetes':satpaquetes,'estado':resultQueryUpdateVerificacion}
		
		if satestado_solicitud == "3":

			pass
	else:
		try:
			cfdi_paquete_mensaje = getinfoFromTb('cfdi_paquetes','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_paquete_mensaje')[0]
		except:
			cfdi_paquete_mensaje = "Sin descargar"
		cfdi_verificacion_numero_cfdi = getinfoFromTb('cfdi_verificacion','cfdi_verificacion_id',cfdi_verificacion_id,'cfdi_verificacion_numero_cfdi')
		cfdi_verificacion_paquetes = getinfoFromTb('cfdi_verificacion','cfdi_verificacion_id',cfdi_verificacion_id,'cfdi_verificacion_paquetes')[0]
		cfdi_verificacion_paquetes = cfdi_verificacion_paquetes.replace("\'", "\"")
		cfdi_verificacion_paquetes = json.loads(cfdi_verificacion_paquetes)
		if cfdi_paquete_mensaje == 'Solicitud Aceptada':
			cfdi_paquete_location = getinfoFromTb('cfdi_paquetes','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_paquete_location')[0]
			cfdi_paquete_content = getinfoFromTb('cfdi_paquetes','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_paquete_content')[0]
			if cfdi_paquete_content != "Error al obtener los archivos XML dentro del archivo ZIP" and  cfdi_paquete_content != "No existen archivos dentro de la respuesta":
				cfdi_paquete_content = cfdi_paquete_content.replace("\'", "\"")
				cfdi_paquete_content = json.loads(cfdi_paquete_content)
			getDownloadInfo = {'cfdi_paquete_location':cfdi_paquete_location,'cfdi_paquete_content':cfdi_paquete_content,'mensaje':'El paquete ya fue descargado'}
			zip_name_download = cfdi_paquete_location
			zip_download = str(request.META.get('HTTP_HOST')) + '/descarga/zip?aKey=857c4402ad934005eae4638a93812bf7&url=' + zip_name_download
			dir_location = getinfoFromTb('cfdi_paquetes','cfdi_solicitud_id',request.GET['cfdi_solicitud_id'],'cfdi_paquete_src')[0]
			listaddpaquetessat.append(getDownloadInfo)
		else:
			maxRow = len(cfdi_verificacion_paquetes)
			path_location_paquetes = "/home/storage/files/"
			for x in range(maxRow):
				getRequestDownload = getDownloadS(request,cfdi_token_response,str(user_rfc[0]),str(cfdi_verificacion_paquetes[x]),fielg)
				satdcod_estatus = getRequestDownload['descargaPaquete']['cod_estatus']
				satdmensaje = getRequestDownload['descargaPaquete']['mensaje']
				satdpaquete_b64 = getRequestDownload['descargaPaquete']['paquete_b64']
				cfdi_paquete_location_satd_uuid = genUuidv4(request)
				cfdi_paquete_location_satd_name = str(cfdi_solicitud_tipo[0]) + "-" + str(user_rfc[0]) + "-" + cfdi_paquete_location_satd_uuid + ".zip"
				cfdi_paquete_location_satd_dir = path_location_paquetes + cfdi_paquete_location_satd_uuid + "/"
				cfdi_paquete_location_satd = b64toZip(request,satdpaquete_b64,cfdi_paquete_location_satd_name,cfdi_paquete_location_satd_dir)
				cfdi_paquete_location_satd_files = "No existen archivos dentro de la respuesta"
				if cfdi_paquete_location_satd != None:
					cfdi_paquete_location_satd_files = extractZip(request,cfdi_paquete_location_satd_dir+cfdi_paquete_location_satd_name,cfdi_paquete_location_satd_dir,request.GET['cfdi_solicitud_id'])
					pass
				listaddpaquetessat.append(solicitudPaquetes(request,satdcod_estatus,satdmensaje,satdpaquete_b64,cfdi_paquete_location_satd,request.GET['cfdi_solicitud_id'],cfdi_token_id,str(user_rfc[0]),str(cfdi_solicitud_tipo[0]),cfdi_paquete_location_satd_files,cfdi_paquete_location_satd_dir))
		
				pass


		verificacionsatRequestStatus = {'cfdi_verificacion_numero_cfdi':cfdi_verificacion_numero_cfdi,'cfdi_verificacion_paquetes':cfdi_verificacion_paquetes,'mensaje':'Esta solicitud ya fue procesada correctamente'}
	data = {
		'token':[],
		'cfdi_solicitud_id' : request.GET['cfdi_solicitud_id'],
		'estado_solicitud' : querysolicitudxEstado,
		'estado_verificacion':cfdi_verificacion_estado_solicitud,
		'tipo':cfdi_solicitud_tipo,
		'nueva_verificacion':[],
		'paquetes':listaddpaquetessat,
		'sessionData':[],
		'zip_download': zip_download,
		'dir_location':dir_location,
	}
	#querysessionData = sendLog(request.GET['cfdi_solicitud_id'],'cfdi_solicitud_id',request,'verificasolicitud')
	#data['sessionData'].append(querysessionData)
	data['nueva_verificacion'].append(verificacionsatRequestStatus)
	data['token'].append(listaddtokenResponse)

	response = JsonResponse(data,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def downloadFileSat(request):
	data = []
	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'url' not in request.GET :
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		"""
		"""

	file_path = request.GET['url']
	if ("/home/storage/files/" and "zip") in file_path:
		if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/zip")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
				response["Access-Control-Allow-Origin"] = "*"
				return response
		raise Http404
	else:
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	pass

@csrf_exempt
def readXML(request):
	data = {
		"firstChild" : [],
		"childNodes":[]
	}
	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'user_file_location' not in request.GET or 'user_id' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		"""
		"""
	if getinfoFromTb('api_tb_file','user_file_location',request.GET['user_file_location'],'user_file_location') is not None:
		xmlLocation = getinfoFromTb('api_tb_file','user_file_location',request.GET['user_file_location'],'user_file_location')[0]
		try:
			xmlLocation = xmlLocation
			updatexmlStatus = updateinfoFromTb("api_tb_file","file_status","json","user_file_location",request.GET['user_file_location'])
		except:
			data = codemessage(902)
			return JsonResponse(data,safe=False)
			sys.exit();
	else:
		data = codemessage(902)
		return JsonResponse(data,safe=False)
		sys.exit();

	xmlDoc = minidom.parse(xmlLocation)
	xmlFC = xmlDoc.firstChild.tagName
	xmlFCContent = xmlDoc.getElementsByTagName(xmlFC)
	xmlCN = xmlDoc.firstChild.childNodes

	if hasattr(xmlDoc.firstChild, '_attrs'):
		iteminDic = xmlDoc.firstChild._attrs.items()
		for key, value in iteminDic:
			nameElement = key
			value = value.nodeValue
			appendValue = {'elemento':str(nameElement),'valor':str(value)}
			data['firstChild'].append(appendValue)
	else:
		appendValue = {'data':False}
		data['firstChild'].append(appendValue)

	xmllenCN = len(xmlCN)
	for x in range(xmllenCN):
		if hasattr(xmlCN[x], 'tagName'):
			tagName = xmlCN[x].tagName
			if hasattr(xmlCN[x], 'dataXML'):
				"""append data
				"""
			else:
				if hasattr(xmlCN[x], 'childNodes'):
					if len(xmlCN[x].childNodes) == 0:
						if hasattr(xmlCN[x], '_attrs'):
							iteminDic = xmlCN[x]._attrs.items()
							row = {
								tagName:[]
							}
							for key, value in iteminDic:
								nameElement = key
								value = value.nodeValue
								appendValue = {'elemento':str(nameElement),'valor':str(value)}
								row[tagName].append(appendValue)

							data['childNodes'].append(row)	
						else:
							""" dont have attributes in child
							"""
							pass
					else:
						""" More childs in None
						"""
						#1
						row = {tagName:[]}
						data["childNodes"].append(row)
						if hasattr(xmlCN[x], '_attrs'):
							if hasattr(xmlCN[x]._attrs, 'items'):
								iteminDic = xmlCN[x]._attrs.items()
								for key, value in iteminDic:
									nameElement = key
									value = value.nodeValue
									row[tagName].append({'elemento':str(nameElement),'valor':str(value)})	

						xmlCNi= xmlCN[x].childNodes
						xmllenCNi = len(xmlCNi)
						i=0
						for q in range(xmllenCNi):
							if hasattr(xmlCNi[q], 'tagName'):
								tagName1 = xmlCNi[q].tagName
								
								if tagName in row:
									row[tagName].append({tagName1:[]})
								else:
									pass
								if hasattr(xmlCNi[q], 'dataXML'):
									"""append data
									"""
								else:
									if hasattr(xmlCNi[q], 'childNodes'):
										if len(xmlCNi[q].childNodes) == 0:
											if hasattr(xmlCNi[q], '_attrs'):
												iteminDic = xmlCNi[q]._attrs.items()
												
												for key, value in iteminDic:
													nameElement = key
													value = value.nodeValue
													if tagName in row:
														row[tagName][i][tagName1].append({'elemento':str(nameElement),'valor':str(value)})
													else:
														pass
												i = i+ 1
											else:
												""" dont have attributes in child
												"""
												pass
										else:
											""" More childs in None
											"""
											#2

											if hasattr(xmlCNi[q], '_attrs'):
												if hasattr(xmlCNi[q]._attrs, 'items'):
													iteminDic = xmlCNi[q]._attrs.items()
													k = 0;
													for key, value in iteminDic:
														nameElement = key
														value = value.nodeValue
														row[tagName][k][tagName1].append({'elemento':str(nameElement),'valor':str(value)})
														try:
															print(tagName + "" + tagName1)
														except:
															print(tagName + "" + tagName1)

											xmlCNii= xmlCNi[q].childNodes
											xmllenCNii = len(xmlCNii)
											for z in range(xmllenCNii):
												if hasattr(xmlCNii[z], 'tagName'):
													tagName2 = xmlCNii[z].tagName
													if hasattr(xmlCNii[z], 'dataXML'):
														"""append data
														"""
													else:
														if hasattr(xmlCNii[z], 'childNodes'):
															if len(xmlCNii[z].childNodes) == 0:
																if hasattr(xmlCNii[z], '_attrs'):
																	iteminDic = xmlCNii[z]._attrs.items()
																	for key, value in iteminDic:
																		nameElement = key
																		value = value.nodeValue
															

																	#data['childNodes'].append(rowii)	
																else:
																	""" dont have attributes in child
																	"""
																	pass
															else:
																""" More childs in None
																"""

																if hasattr(xmlCNii[z], '_attrs'):
																	if hasattr(xmlCNii[z]._attrs, 'items'):
																		iteminDic = xmlCNii[z]._attrs.items()
																		for key, value in iteminDic:
																			nameElement = key
																			value = value.nodeValue

																xmlCNiii= xmlCNii[z].childNodes
																xmllenCNiii = len(xmlCNiii)
																for m in range(xmllenCNiii):
																	if hasattr(xmlCNiii[m], 'tagName'):
																		tagName = xmlCNiii[m].tagName
																		if hasattr(xmlCNiii[m], 'dataXML'):
																			"""append data
																			"""
																		else:
																			if hasattr(xmlCNiii[m], 'childNodes'):
																				if len(xmlCNiii[m].childNodes) == 0:
																					if hasattr(xmlCNiii[m], '_attrs'):
																						iteminDic = xmlCNiii[m]._attrs.items()
																						for key, value in iteminDic:
																							nameElement = key
																							value = value.nodeValue
																					else:
																						""" dont have attributes in child
																						"""
																						pass
																				else:
																					""" More childs in None
																					"""

																					if hasattr(xmlCNiii[m], '_attrs'):
																						if hasattr(xmlCNiii[m]._attrs, 'items'):
																							iteminDic = xmlCNiii[m]._attrs.items()
																							for key, value in iteminDic:
																								nameElement = key
																								value = value.nodeValue
																								appendValue = {'elemento':str(nameElement),'valor':str(value)}
																								if tagName in row:
																									try:
																										row[tagName].append(appendValue)

																										try:
																											print(tagName)
																										except:
																											print(tagName)
																									except:
																										print("fuera de rango")
																								else:
																									pass
																									
																					xmlCNiiii= xmlCNiii[m].childNodes
																					xmllenCNiiii = len(xmlCNiiii)
																					for u in range(xmllenCNiiii):
																						if hasattr(xmlCNiiii[u], 'tagName'):
																							tagName = xmlCNiiii[u].tagName
																							if hasattr(xmlCNiiii[u], 'dataXML'):
																								"""append data
																								"""
																							else:
																								if hasattr(xmlCNiiii[u], 'childNodes'):
																									if len(xmlCNiiii[u].childNodes) == 0:
																										if hasattr(xmlCNiiii[u], '_attrs'):
																											iteminDic = xmlCNiiii[u]._attrs.items()
																											for key, value in iteminDic:
																												nameElement = key
																												value = value.nodeValue
																										else:
																											""" dont have attributes in child
																											"""
																											pass
																									else:
																										""" More childs in None
																										"""
																					
														else:
															"""no attribute exists childNodes
															"""
															pass
												else:
													"""no attribute exists tagName
													"""
													pass
									else:
										"""no attribute exists childNodes
										"""
										pass
							else:
								"""no attribute exists tagName
								"""
								pass
				else:
					"""no attribute exists childNodes
					"""
					pass
		else:
			"""no attribute exists tagName
			"""
			pass
	response = JsonResponse(data,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def solicitudPoliza(request):
	results ={
		"user_rfc":[],
		"fecha":[],
		"file_id":[],
		"data":[],
		"poliza_details":[],
		"template":[]	
	}
	getJson = request.read()
	try:
		data = json.loads(getJson)
		try:
			pass
		except:
			data = codemessage(909)
			return JsonResponse(data,safe=False)
			sys.exit();
	except:
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	queryaccessKey = accessKey(request,data[0]['api_key'])
	if queryaccessKey  is None:
		data = codemessage(901)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass
	totalItems = len(data[1])
	for i in range(0, totalItems):
		if 'origen'  in data[1][i].keys() and 'destino' in data[1][i].keys():

			origenData = data[1][i]['origen']
			destinoData = data[1][i]['destino']

			elementoO = origenData['elemento']
			valorO = origenData['valor']

			elementoD = destinoData['elemento']
			valorD = destinoData['valor']
			if elementoO == "RFC" :
				value = {
					'user_rfc':valorO
					}
				results['user_rfc'].append(value)
			elif 'rango' in elementoO:
				value = {
					'poliza_date_search':valorO
					}
				results['fecha'].append(value)
			elif 'file_id' in elementoO:
				value = {
					'file_id':valorO
					}
				results['file_id'].append(value)
			else:
				k = str(elementoD)
				row = {k:[]}
				value = {
					'index_key_origin':elementoO,
					'index_value_origin':valorO,
					'index_key_destination':elementoD,
					'index_value_destination':""
					}
				row[k].append(value)
				results['data'].append(row)
		else:
			data = codemessage(910)
			return JsonResponse(data,safe=False)
			sys.exit();
	if(data[0]['template'] == ""):
		template_name = data[0]['template_name']
		results['template'].append({"action": "selected","name": data[0]['template_name']})
	else: 
		template_name = results['user_rfc'][0]['user_rfc'] + "_" + data[0]['template_name'] 
	
	if(data[0]['template'] == "add"):
		queryInsertTemplate = insertaTemplate(results['user_rfc'][0]['user_rfc'],template_name,data[0]['template_params']);
		results['template'].append({"action": data[0]['template'],"name": template_name,"content":data[0]['template_params']})

	queryInsertPoliza = insertarPoliza(results['user_rfc'][0]['user_rfc'],results['fecha'][0]['poliza_date_search'],results['file_id'][0]['file_id'],results['data'],template_name)

	if queryInsertPoliza  is None:
		data = codemessage(911)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		queryInsertPoliza = str(request.META.get('HTTP_HOST')) + "/descarga/details/poliza?poliza_id=" + str(queryInsertPoliza)
		results['poliza_details'].append(queryInsertPoliza)
		pass
	
	response = JsonResponse(results,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def detailsPoliza(request):
	results ={
		"query":[],
		"search":[],
	}

	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'poliza_id' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	user_rfc = getinfoFromTb("cfdi_poliza","poliza_id",request.GET['poliza_id'],"user_rfc")[0]
	poliza_date_search = getinfoFromTb("cfdi_poliza","poliza_id",request.GET['poliza_id'],"poliza_date_search")[0]
	file_id = getinfoFromTb("cfdi_poliza","poliza_id",request.GET['poliza_id'],"file_id")[0]
	poliza_data = getinfoFromTb("cfdi_poliza","poliza_id",request.GET['poliza_id'],"poliza_data")[0]
	poliza_data = poliza_data.replace("\'", "\"")
	poliza_data = json.loads(poliza_data)
	poliza_date_created = getinfoFromTb("cfdi_poliza","poliza_id",request.GET['poliza_id'],"poliza_date_created")[0]
	
	query = {'user_rfc':user_rfc,'poliza_date_search':poliza_date_search,'file_id':file_id,'poliza_data':poliza_data,'poliza_date_created':poliza_date_created}
	results['query'].append(query)
	
	querySearchPoliza = searchcfdiIndex(poliza_date_search,user_rfc)
	if querySearchPoliza  is None:
		data = codemessage(912)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass
	results['search'].append(querySearchPoliza)

	response = JsonResponse(results,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def searchPoliza(request):
	results ={
		"query":[],
		"search":[],
	}

	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'user_rfc' not in request.GET or 'date' not in request.GET or 'user_id' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	queryRFC = getUserRfc(request.GET['user_id'],request.GET['user_rfc'])
	if len(queryRFC)  == 0:
		data = codemessage(913)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	date = request.GET['date']
	date = date.split("|")
	try:
		iDate = date[0].split("-")
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();

		eDate = date[1].split("-")
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();

		YiDate = iDate[0]
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();
		MiDate = iDate[1]
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();
		YeDate = eDate[0]
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();
		MeDate = eDate[1]
		try:
			pass
		except:
			data = codemessage(400)
			return JsonResponse(data,safe=False)
			sys.exit();
	except:
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
		
	if(YiDate == YeDate):
		if (int(MiDate) != int(MeDate)):
			for i in range(int(MiDate), int(MeDate)):
				getDate = YiDate + "-" + "{:02d}".format(i)
				querySearchPolizaUser = searchPolizaC(request,getDate,request.GET['user_rfc'])
				if len(querySearchPolizaUser)  == 0:
					pass
				else:
					results['search'].append(querySearchPolizaUser)
		else:
			getDate = YiDate + "-" + "{:02d}".format(int(MiDate))
			querySearchPolizaUser = searchPolizaC(request,getDate,request.GET['user_rfc'])
			if len(querySearchPolizaUser)  == 0:
				pass
			else:
				results['search'].append(querySearchPolizaUser)

	else:
		for i in range(int(MiDate), 12):
			getDate = YiDate + "-" + "{:02d}".format(i)
			querySearchPolizaUser = searchPolizaC(request,getDate,request.GET['user_rfc'])
			if len(querySearchPolizaUser)  == 0:
				pass
			else:
				results['search'].append(querySearchPolizaUser)

		for i in range(1, int(MeDate)):
			getDate = YeDate  + "-" + "{:02d}".format(i)
			querySearchPolizaUser = searchPolizaC(request,getDate,request.GET['user_rfc'])
			if len(querySearchPolizaUser)  == 0:
				pass
			else:
				results['search'].append(querySearchPolizaUser)


	
	

	results['query'].append({'user_rfc':request.GET['user_rfc'],'user_id':request.GET['user_id'],'date':request.GET['date']})	
	response = JsonResponse(results,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response


@csrf_exempt
def removeItemCfdi(request):
	results ={
		"query":[],
		"search":[],
	}

	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'from' not in request.GET or 'key' not in request.GET or 'value' not in request.GET or 'user_id' not in request.GET or 'user_rfc' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	if authrItems(request.GET['from'],request.GET['key']) == None:
		data = codemessage(914)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	queryRFC = getUserRfc(request.GET['user_id'],request.GET['user_rfc'])
	if len(queryRFC)  == 0:
		data = codemessage(913)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	results['query'].append({"index":request.GET['from'],"identifier":request.GET['key'],"value":request.GET['value'],'user_id':request.GET['user_id'],'user_rfc':request.GET['user_rfc']})

	queryRemoveItem = deleteinfoFromTbcfdi(request.GET['from'],request.GET['key'],request.GET['value'],request.GET['user_rfc'])
	if queryRemoveItem == None:
		data = codemessage(915)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		results['search'].append(queryRemoveItem)

	response = JsonResponse(results,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response

@csrf_exempt
def templatesbyUser(request):
	results ={
		"query":[],
		"search":[],
	}

	vAK = validateAccessKey(request)
	if vAK is True:
		"""
		"""
	else:
		data = vAK
		return JsonResponse(data,safe=False)
		sys.exit();

	if 'user_rfc' not in request.GET:
		"""
			if any parameter  not found in the request
		"""
		data = codemessage(400)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		pass

	user_rfc = request.GET['user_rfc']

	queryTemplate = templatesByRFC(user_rfc)
	if queryTemplate == None:
		data = codemessage(404)
		return JsonResponse(data,safe=False)
		sys.exit();
	else:
		results['search'].append(queryTemplate)
		results['query'].append({"user_rfc" : user_rfc})

	response = JsonResponse(results,safe=False)
	response["Access-Control-Allow-Origin"] = "*"
	return response