import sys

def satEstado(code):

	satMessage = "Desconocido"
	if code == "1":
		satMessage = "Tu solicitud fue aceptada el estado es 1"
	elif code == "2":
		satMessage = "Tu solicitud esta en proceso el estado es 2"
	elif code == "3":
		satMessage = "Tu solicitud fue procesada correctamente el estado es 3 , puedes descargar los paquetes"
	elif code == "4":
		satMessage = "Desconocido"
	elif code == "5":
		satMessage = "Tu solicitud fue rechazada , los parametros con los que fue solicitada son repetidos"
	
	return satMessage

def codemessage(code):
	data = {
		'message':[]
	}
	codeMessage = {"status":503,"message":"Servicio no disponible temporalmente"}
	if code == 400:
		codeMessage = {"status":400,"message":"La petición que solicitas no cumple con el formato"}
	elif code == 401:
		codeMessage = {"status":401,"message":"Autorización requerida"}
	elif code == 403:
		codeMessage = {"status":403,"message":"Acceso prohibido"}
	elif code == 404:
		codeMessage = {"status":404,"message":"Registro no encontrado"}
	elif code == 408:
		codeMessage = {"status":408,"message":"La petición excedio el tiempo de la respuesta"}
	elif code == 410:
		codeMessage = {"status":410,"message":"La solicitud no fue procesada"}
	elif code == 900:
		codeMessage = {"status":False,"message":"Necesitas una llave de acceso"}
	elif code == 901:
		codeMessage = {"status":False,"message":"Tu llave de acceso no es valida"}
	elif code == 902:
		codeMessage = {"status":False,"message":"Archivos no encontrados"}
	elif code == 903:
		codeMessage = {"status":False,"message":"Existe un error al subir los archivos"}
	elif code == 904:
		codeMessage = {"status":False,"message":"Llave privada invalida"}
	elif code == 905:
		codeMessage = {"status":False,"message":"Certificado invalido"}
	elif code == 906:
		codeMessage = {"status":False,"message":"Clave secreta invalida"}
	elif code == 907:
		codeMessage = {"status":False,"message":"Los datos de tu llave privada , certificado o clave secreta contienen errores"}
	elif code == 908:
		codeMessage = {"status":False,"message":"El numero de intentos para obtener un token excedió"}
	elif code == 909:
		codeMessage = {"status":False,"message":"Json no encontrado"}
	elif code == 910:
		codeMessage = {"status":False,"message":"El archivo json no cumple con el formato"}
	elif code == 911:
		codeMessage = {"status":False,"message":"Existe un error al guardar los datos de la poliza"}
	elif code == 912:
		codeMessage = {"status":False,"message":"No se cuentran resultado para la consulta solicitada en el indice de archivos"}	
	elif code == 913:
		codeMessage = {"status":False,"message":"El RFC consultado no se encuentra en tu cuenta"}
	elif code == 914:
		codeMessage = {"status":False,"message":"La consulta que solicitas no esta permitida"}
	elif code == 915:
		codeMessage = {"status":False,"message":"La petición que solicitas no puede ser procesada"}
	data['message'].append(codeMessage)
	return data