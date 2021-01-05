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
import uuid
import base64
import datetime
from hashlib import sha1
import hmac
from .engine import Autenticacion
from .engine import Fiel
from .engine import SolicitaDescarga
from .engine import VerificaSolicitudDescarga
from .engine import DescargaMasiva
import zipfile

def sendLog(log_value_key,log_description_key,request,action):
	querysessionData = logInfo(log_value_key,log_description_key,request,action)
	if querysessionData  is None:
		querysessionData  = codemessage(404)
	else:
		"""
		"""
	return querysessionData

def authrItems(nameItem,key):
	data = None
	authorizedItems = ["cfdi_poliza","cfdi_solicitud"]
	if nameItem in authorizedItems:
		if nameItem == "cfdi_poliza":
			if(key == "poliza_id"):
				data = True
		if nameItem == "cfdi_solicitud":
			if key == "cfdi_solicitud_id":
				data = True
	return data


def validateAccessKey(request):
	if 'aKey' not in request.GET:
		data = []
		data.append(codemessage(900))
		data = data[0]
	else:
		queryaccessKey = accessKey(request,request.GET['aKey'])
		if queryaccessKey  is None:
			data = []
			data.append(codemessage(901))
			data = data[0]

		else:
			data = True
			#sendLog(request.GET['aKey'],'access key',request,'access to api')

	return data
@csrf_exempt
def validateAccessKeyPost(request):
	if 'aKey' not in request.POST:
		data = []
		data.append(codemessage(900))
		data = data[0]
	else:
		queryaccessKey = accessKey(request,request.POST['aKey'])
		if queryaccessKey  is None:
			data = []
			data.append(codemessage(901))
			data = data[0]

		else:
			data = True
			sendLog(request.POST['aKey'],'access key',request,'access to api')

	return data

def fiel(request,cerLocation,keyLocation,secretPassword):
	cer_der = open(cerLocation, 'rb').read()
	key_der = open(keyLocation, 'rb').read() 
	fiel = Fiel(cer_der, key_der, secretPassword)
	return fiel

def getToken(request,rfc,fiel):
	auth = Autenticacion(fiel)
	token = auth.obtener_token()
	try:
		token = auth.obtener_token()
	except:
		token = None
	return token

def requestDownload(request,rfc,token,dateCreated,dateExpires,fiel,tipo_solicitud):
	descarga = SolicitaDescarga(fiel)
	rfc_solicitante = rfc
	rfc_emisor = rfc
	rfc_receptor = rfc

	resultEmitidos = descarga.solicitar_descarga(token, rfc_solicitante, dateCreated, dateExpires,tipo_solicitud, rfc_emisor=rfc_emisor)
	resultsRecibidos = descarga.solicitar_descarga(token, rfc_solicitante, dateCreated, dateExpires,tipo_solicitud, rfc_receptor=rfc_receptor)
	
	data = {
		"solicitudDescargaEmitidos": resultEmitidos,
		"solicitudDescargaRecibidos": resultsRecibidos,
	}
	
	return data

def verifyDownload(request,token,rfc,idResultEmitidos,idResultsRecibidos,fiel):
	v_descarga = VerificaSolicitudDescarga(fiel)
	rfc_solicitante = rfc

	resultEmitidos = v_descarga.verificar_descarga(token, rfc_solicitante, idResultEmitidos)
	resultsRecibidos = v_descarga.verificar_descarga(token, rfc_solicitante, idResultsRecibidos)

	data = {
		"verificacionSolicitudDescargaEmitidos": resultEmitidos,
		"verificacionSolicitudDescargaRecibidos": resultsRecibidos,
	}
	
	return data

def verifyDownloadE(request,token,rfc,idResultEmitidos,fiel):
	v_descarga = VerificaSolicitudDescarga(fiel)
	rfc_solicitante = rfc[0]

	resultEmitidos = v_descarga.verificar_descarga(token, rfc_solicitante, idResultEmitidos)

	data = {
		"verificacionSolicitudDescargaEmitidos": resultEmitidos
	}
	
	return data

def verifyDownloadR(request,token,rfc,idResultsRecibidos,fiel):
	v_descarga = VerificaSolicitudDescarga(fiel)
	rfc_solicitante = rfc[0]

	resultsRecibidos = v_descarga.verificar_descarga(token, rfc_solicitante, idResultsRecibidos)

	data = {
		"verificacionSolicitudDescargaRecibidos": resultsRecibidos,
	}
	
	return data

def getDownload(request,token,rfc,idResultEmitidos,idResultsRecibidos,fiel):
	descarga = DescargaMasiva(fiel)
	rfc_solicitante = rfc 

	resultEmitidos = descarga.descargar_paquete(token, rfc_solicitante, idResultEmitidos)
	resultsRecibidos = descarga.descargar_paquete(token, rfc_solicitante, idResultsRecibidos)
	data = {
		"descargaEmitidos": resultEmitidos,
		"descargaRecibidos": resultsRecibidos,
	}

	return data

def getDownloadS(request,token,rfc,idPaquete,fiel):
	descarga = DescargaMasiva(fiel)
	rfc_solicitante = rfc 

	result = descarga.descargar_paquete(token, rfc_solicitante, idPaquete)
	data = {
		"descargaPaquete": result,
	}

	return data

def authSat(request,xml):
	urlWS = wsSat("autenticacion")
	headers = {'Content-Type': 'application/xml'}
	response = requests.post(urlWS, data=xml, headers=headers).text
	return response

def formatDate(request,date):#20200604T0001
	dt = datetime.datetime.strptime(date, '%Y%m%dT%H%M%S')
	dt = dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
	return str(dt)

def genUuidv4(request):
	uuidOutput = str(uuid.uuid4())
	uuidOutput = uuidOutput
	return uuidOutput

def b64toZip(request,b64,file_name,path_location):
	if b64 is None:
		fullname = None
	else:
		try:
			os.mkdir(path_location)
			fullname =  path_location + file_name
			decoded = base64.b64decode(b64)
			with open(fullname, 'wb') as f:
				f.write(decoded)
		except OSError:
		    print ("Error al crear el directorio %s" % path)
		    fullname = None
	return fullname

def extractZip(request,fileLocation,putLocation,cfdi_solicitud_id):
	listfileinZip = ""
	try:
		with zipfile.ZipFile(fileLocation, 'r') as zip_ref:
			 zip_ref.extractall(putLocation)
			 listfileinZip = zip_ref.namelist()
	except:
		listfileinZip = "Error al obtener los archivos XML dentro del archivo ZIP"

	if listfileinZip != "Error al obtener los archivos XML dentro del archivo ZIP":
		from xml.dom import minidom
		itemsinZip = len(listfileinZip)
		for x in range(itemsinZip):
			cfdi_solicitud_id = cfdi_solicitud_id
			cfdi_index_source = putLocation + listfileinZip[x]
			xmlDoc= minidom.parse(putLocation + listfileinZip[x])

			cfdiComprobante = xmlDoc.getElementsByTagName('cfdi:Comprobante')
			cfdi_index_FormaPago = cfdiComprobante[0].getAttribute("FormaPago")
			cfdi_index_MetodoPago = cfdiComprobante[0].getAttribute("MetodoPago")
			cfdi_index_Moneda = cfdiComprobante[0].getAttribute("Moneda")
			cfdi_index_SubTotal = cfdiComprobante[0].getAttribute("SubTotal")
			cfdi_index_TipoDeComprobante = cfdiComprobante[0].getAttribute("TipoDeComprobante")
			cfdi_index_Total = cfdiComprobante[0].getAttribute("Total")

			cfdiEmisor = xmlDoc.getElementsByTagName('cfdi:Emisor')
			cfdi_index_Emisor_Rfc = cfdiEmisor[0].getAttribute("Rfc")
			cfdi_index_Emisor_Nombre = cfdiEmisor[0].getAttribute("Nombre")

			cfdiReceptor = xmlDoc.getElementsByTagName('cfdi:Receptor')
			cfdi_index_Receptor_Rfc = cfdiReceptor[0].getAttribute("Rfc")
			cfdi_index_Receptor_Nombre = cfdiReceptor[0].getAttribute("Nombre")

			cfdiComplemento = xmlDoc.getElementsByTagName('cfdi:Complemento')
			tfdTimbreFiscalDigital = cfdiComplemento[0].getElementsByTagName('tfd:TimbreFiscalDigital')
			cfdi_index_SelloSAT = tfdTimbreFiscalDigital[0].getAttribute("SelloSAT")
			cfdi_index_FechaTimbrado = tfdTimbreFiscalDigital[0].getAttribute("FechaTimbrado")
			
			cfdi_index(cfdi_solicitud_id,cfdi_index_FechaTimbrado,cfdi_index_FormaPago,cfdi_index_SubTotal,cfdi_index_Moneda,cfdi_index_Total,cfdi_index_TipoDeComprobante,cfdi_index_MetodoPago,cfdi_index_Emisor_Rfc,cfdi_index_Emisor_Nombre,cfdi_index_Receptor_Rfc,cfdi_index_Receptor_Nombre,cfdi_index_SelloSAT,cfdi_index_source)		
	
	return listfileinZip
