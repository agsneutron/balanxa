import sys
from django.db import connections
from datetime import datetime
import socket
now = datetime.now()
datetimeCurrent = now.strftime("%Y-%m-%d %H:%M:%S")

def updateinfoFromTb(table,keyUpdate,valueUpdate,keyCond,valueCond):
	cursor = connections['default'].cursor()
	cursor.execute("UPDATE "+table+" SET "+keyUpdate+"=%s WHERE "+keyCond+"=%s ",[valueUpdate,valueCond])
	try:
		row = {'sucess':True,'keyUpdate': keyUpdate,'valueUpdate':valueUpdate ,'keyCond':keyCond,'valueCond':valueCond}
	except:
		row = None
	
	return row

def deleteinfoFromTbcfdi(table,keyCond,valueCond,user_rfc):
	row2 = ""
	row3 = ""
	row4 = ""
	cursor = connections['default'].cursor()
	cursor.execute("DELETE FROM "+table+" WHERE "+keyCond+"=%s AND user_rfc=%s",[valueCond,user_rfc])
	row = cursor.rowcount

	if table == "cfdi_solicitud":
		cursor.execute("DELETE FROM cfdi_index WHERE cfdi_solicitud_id=%s",[valueCond])
		row2 = cursor.rowcount

		cursor.execute("DELETE FROM cfdi_paquetes WHERE cfdi_solicitud_id=%s",[valueCond])
		row3 = cursor.rowcount

		cursor.execute("DELETE FROM cfdi_verificacion WHERE cfdi_solicitud_id=%s",[valueCond])
		row4 = cursor.rowcount

	
	if row == 0 :
		row = {'sucess':False,'message':'No se encontraron registros para borrar','rows affected':row}
	else:
		row = {'sucess':True,'keyCond':keyCond,'valueCond':valueCond,'rows affected':row,'other rows affected': row2 + row3 + row4}
	
	return row
	
def accessKey(request,accesskey):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT access_id FROM api_tb_access WHERE access_key=%s",[accesskey])
	row = cursor.fetchone()
	if row is None:
		data = row
	else:
		data ={'success':True}
	return data

def logInfo(log_value_key,log_description_key,request,action):
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO api_tb_log(log_action,log_ip_user,log_value_key,log_date,log_description_key) VALUES(%s,%s,%s,%s,%s)",[action,request.META.get('REMOTE_ADDR'),log_value_key,datetimeCurrent,log_description_key])
	try:
		row = True
		data = {'sucess':row,'log_action':action,'log_ip_user':request.META.get('REMOTE_ADDR'),'log:date':datetimeCurrent}
	except:
		row = "error"
		data = None	

	return data

def guardaToken(request,user_rfc,cfdi_token_response):
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_token(user_rfc,cfdi_token_response,cfdi_token_date) VALUES(%s,%s,%s)",[user_rfc,cfdi_token_response,datetimeCurrent])
	try:
		currentId = cursor.lastrowid
		row = True
		data = {'sucess':row,'action':'solicita token','cfdi_token_id':currentId,'cfdi_token_response':cfdi_token_response,'cfdi_token_date':datetimeCurrent}
	except:
		row = "error"
		data = None	

	return data

def buscaToken(request,cfdi_token_id):
	pass

def guardaSolicitud(request,cfdi_solicitud_sat_id,cfdi_solicitud_cod_estatus,cfdi_solicitud_mensaje,cfdi_token_id,cfdi_solicitud_tipo,user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf):
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_solicitud(cfdi_solicitud_sat_id,cfdi_solicitud_cod_estatus,cfdi_solicitud_mensaje,cfdi_solicitud_date,cfdi_token_id,cfdi_solicitud_tipo,user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[cfdi_solicitud_sat_id,cfdi_solicitud_cod_estatus,cfdi_solicitud_mensaje,datetimeCurrent,cfdi_token_id,cfdi_solicitud_tipo,user_rfc,cfdi_solicitud_rango,cfdi_solicitud_pdf])
	try:
		currentId = cursor.lastrowid
		row = True
		data = {'sucess':row,'action':'envia solicitud','cfdi_solicitud_id':currentId,'cfdi_solicitud_sat_id':cfdi_solicitud_sat_id,'cfdi_solicitud_cod_estatus':cfdi_solicitud_cod_estatus,'cfdi_solicitud_mensaje':cfdi_solicitud_mensaje,'cfdi_solicitud_date':datetimeCurrent,'cfdi_solicitud_tipo':cfdi_solicitud_tipo}
	except:
		row = "error"
		data = None	

	return data

def buscaSolicitud(request,cfdi_solicitud_id):
	pass

def guardaValidacion(request,cfdi_validacion_cod_estatus,cfdi_validacion_estado,cfdi_validacion_ec,cfdi_validacion_total,cfdi_validacion_identificador,user_rfc):
	pass

def buscaValidacion(request,cfdi_validacion_id):
	pass

def guardaVerificacion(request,cfdi_verificacion_cod_estatus,cfdi_verificacion_estado_solicitud,cfdi_verificacion_cod_estado_solicitud,cfdi_verificacion_numero_cfdi,cfdi_verificacion_mensaje,cfdi_solicitud_id,cfdi_token_id,cfdi_verificacion_tipo,user_rfc,estado_verificacion):
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_verificacion(cfdi_verificacion_cod_estatus,cfdi_verificacion_estado_solicitud,cfdi_verificacion_cod_estado_solicitud,cfdi_verificacion_numero_cfdi,cfdi_verificacion_mensaje,cfdi_solicitud_id,cfdi_token_id,cfdi_verificacion_date,cfdi_verificacion_tipo,user_rfc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[cfdi_verificacion_cod_estatus,estado_verificacion,cfdi_verificacion_cod_estado_solicitud,cfdi_verificacion_numero_cfdi,cfdi_verificacion_mensaje,cfdi_solicitud_id,cfdi_token_id,datetimeCurrent,cfdi_verificacion_tipo,user_rfc])
	try:
		currentId = cursor.lastrowid
		row = True
		data = {'sucess':row,'action':'verifica solicitud','cfdi_verificacion_id':currentId,'cfdi_verificacion_cod_estatus':cfdi_verificacion_cod_estatus,'cfdi_verificacion_mensaje':cfdi_verificacion_mensaje,'cfdi_verificacion_numero_cfdi':cfdi_verificacion_numero_cfdi,'cfdi_verificacion_date':datetimeCurrent,'cfdi_solicitud_id':cfdi_solicitud_id,'cfdi_verificacion_cod_estado_solicitud':estado_verificacion}
	except:
		row = "error"
		data = None	

	return data

def buscaVerificacion(request,cfdi_verificacion_id):
	pass

def solicitudPaquetes(request,cfdi_paquete_cod_estatus,cfdi_paquete_mensaje,cfdi_paquete_b_64,cfdi_paquete_location,cfdi_solicitud_id,cfdi_token_id,user_rfc,cfdi_paquete_tipo,cfdi_paquete_content,cfdi_paquete_src):
	cfdi_paquete_b_64 = ""
	cfdi_paquete_content = str(cfdi_paquete_content)
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_paquetes(cfdi_paquete_cod_estatus,cfdi_paquete_mensaje,cfdi_paquete_b_64,cfdi_paquete_location,cfdi_solicitud_id,cfdi_token_id,user_rfc,cfdi_paquete_date,cfdi_paquete_tipo,cfdi_paquete_content,cfdi_paquete_src) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[cfdi_paquete_cod_estatus,cfdi_paquete_mensaje,cfdi_paquete_b_64,cfdi_paquete_location,cfdi_solicitud_id,cfdi_token_id,user_rfc,datetimeCurrent,cfdi_paquete_tipo,cfdi_paquete_content,cfdi_paquete_src])
	try:
		currentId = cursor.lastrowid
		row = True
		cfdi_paquete_content = cfdi_paquete_content.replace("\'", "\"")
		cfdi_paquete_content = json.loads(cfdi_paquete_content)
		data = {'sucess':row,'action':'descaga paquetes','cfdi_paquete_id':currentId,'cfdi_paquete_location':cfdi_paquete_location,'cfdi_paquete_cod_estatus':cfdi_paquete_cod_estatus,'cfdi_paquete_mensaje':cfdi_paquete_mensaje,'cfdi_solicitud_id':cfdi_solicitud_id,'cfdi_paquete_content':cfdi_paquete_content}
	except:
		row = "error"
		data = None	

	return data

def buscaPaquetes(request,cfdi_paquete_id):
	pass

def solicitudesporRFC(request,user_rfc):
	data =[]
	cursor = connections['default'].cursor()
	cursor.execute("SELECT cfdi_solicitud_id,cfdi_solicitud_sat_id,cfdi_solicitud_mensaje,cfdi_solicitud_tipo,cfdi_solicitud_date,cfdi_solicitud_rango,cfdi_solicitud_pdf FROM cfdi_solicitud WHERE user_rfc=%s ORDER BY cfdi_solicitud_date DESC",[user_rfc])
	row = cursor.fetchall()
	if not row:
		data = None
	else:
		maxRow = len(row)
		for x in range(maxRow):
			cfdi_verificacion_id = getinfoFromTb('cfdi_verificacion','cfdi_solicitud_id',row[x][0],'cfdi_verificacion_id')
			cfdi_verificacion_estado_solicitud = getinfoFromTb('cfdi_verificacion','cfdi_verificacion_id',cfdi_verificacion_id,'cfdi_verificacion_estado_solicitud')
			data.append({'cfdi_verificacion_estado_solicitud':cfdi_verificacion_estado_solicitud,'user_rfc':user_rfc,'cfdi_solicitud_rango':row[x][5],'cfdi_solicitud_id':row[x][0],'cfdi_solicitud_sat_id':row[x][1],'cfdi_solicitud_mensaje':row[x][2],'cfdi_solicitud_tipo':row[x][3],'cfdi_solicitud_date':row[x][4],'cfdi_solicitud_pdf':row[x][6],'api_url_verifica_solicitud':str(request.META.get('HTTP_HOST')) +'/descarga/verifica?cfdi_solicitud_id=' + str(row[x][0]) + '&cfdi_solicitud_sat_id=' + str(row[x][1]) + '&aKey=' + str(request.GET['aKey'])})

	return data

def verificaSolicitudEstado(request,cfdi_solicitud_id):
	pass

def getinfoFromTb(table,key,value,field):
	cursor = connections['default'].cursor()
	cursor.execute("SELECT "+field+" from "+table+" WHERE "+key+"=%s",[value])
	row = cursor.fetchone()
	return row

def actualizaVerificacion(cfdi_verificacion_cod_estatus,cfdi_verificacion_mensaje,cfdi_verificacion_estado_solicitud,cfdi_verificacion_cod_estado_solicitud,cfdi_verificacion_numero_cfdi,cfdi_verificacion_paquetes,cfdi_verificacion_id):
	cfdi_verificacion_paquetes = str(cfdi_verificacion_paquetes)
	cursor = connections['default'].cursor()
	cursor.execute("UPDATE cfdi_verificacion SET cfdi_verificacion_cod_estatus=%s,cfdi_verificacion_mensaje=%s,cfdi_verificacion_estado_solicitud=%s,cfdi_verificacion_cod_estado_solicitud=%s,cfdi_verificacion_numero_cfdi=%s,cfdi_verificacion_paquetes=%s WHERE cfdi_verificacion_id=%s ",[cfdi_verificacion_cod_estatus,cfdi_verificacion_mensaje,cfdi_verificacion_estado_solicitud,cfdi_verificacion_cod_estado_solicitud,cfdi_verificacion_numero_cfdi,cfdi_verificacion_paquetes,cfdi_verificacion_id])
	try:
		row = True
	except:
		row = "hubo un error al actualizar la información"	
	return row

def cfdi_index(cfdi_solicitud_id,cfdi_index_FechaTimbrado,cfdi_index_FormaPago,cfdi_index_SubTotal,cfdi_index_Moneda,cfdi_index_Total,cfdi_index_TipoDeComprobante,cfdi_index_MetodoPago,cfdi_index_Emisor_Rfc,cfdi_index_Emisor_Nombre,cfdi_index_Receptor_Rfc,cfdi_index_Receptor_Nombre,cfdi_index_SelloSAT,cfdi_index_source):
	data = []
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_index(cfdi_solicitud_id,cfdi_index_FechaTimbrado,cfdi_index_FormaPago,cfdi_index_SubTotal,cfdi_index_Moneda,cfdi_index_Total,cfdi_index_TipoDeComprobante,cfdi_index_MetodoPago,cfdi_index_Emisor_Rfc,cfdi_index_Emisor_Nombre,cfdi_index_Receptor_Rfc,cfdi_index_Receptor_Nombre,cfdi_index_SelloSAT,cfdi_index_source) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[cfdi_solicitud_id,cfdi_index_FechaTimbrado,cfdi_index_FormaPago,cfdi_index_SubTotal,cfdi_index_Moneda,cfdi_index_Total,cfdi_index_TipoDeComprobante,cfdi_index_MetodoPago,cfdi_index_Emisor_Rfc,cfdi_index_Emisor_Nombre,cfdi_index_Receptor_Rfc,cfdi_index_Receptor_Nombre,cfdi_index_SelloSAT,cfdi_index_source])
	try:
		currentId = cursor.lastrowid
		row = True
	except:
		row = "error"
		data = None	

	return data

def getUserFile(user_id):
	data = []
	cursor = connections['default'].cursor()
	cursor.execute("SELECT file_id, user_id, user_file_location  from api_tb_file WHERE user_id=%s",[user_id])
	row = cursor.fetchall()
	if row is None:
		data = row
	else:
		maxRow = len(row)
		for x in range(maxRow):
			data.append({'file_id': row[x][0],'user_id':row[x][1],'user_file_location':row[x][2]})
	return data

def insertarPoliza(user_rfc,poliza_date_search,file_id,poliza_data,poliza_template):
	poliza_data  = str(poliza_data)
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO cfdi_poliza(user_rfc,poliza_date_search,file_id,poliza_data,poliza_date_created,poliza_template) VALUES(%s,%s,%s,%s,%s,%s)",[user_rfc,poliza_date_search,file_id,poliza_data,datetimeCurrent,poliza_template])
	try:
		currentId = cursor.lastrowid
		row = True
		data = currentId
	except:
		row = "error"
		data = None	

	return data

def searchcfdiIndex(date,user_rfc):
	data = {
		"Emisor":[],
		"Receptor":[]
	}
	cursor = connections['default'].cursor()
	cursor.execute("SELECT DISTINCT cfdi_index_FechaTimbrado,cfdi_index_FormaPago,cfdi_index_SubTotal,cfdi_index_Moneda,cfdi_index_Total,cfdi_index_TipoDeComprobante,cfdi_index_MetodoPago,cfdi_index_Emisor_Rfc,cfdi_index_Emisor_Nombre,cfdi_index_Receptor_Rfc,cfdi_index_Receptor_Nombre,cfdi_index_SelloSAT,cfdi_index_source  from cfdi_index WHERE cfdi_index_FechaTimbrado LIKE '%"+date+"%' AND  (cfdi_index_Emisor_Rfc='"+user_rfc+"' OR cfdi_index_Receptor_Rfc='"+user_rfc+"')")
	row = cursor.fetchall()
	if row is None:
		data = None
	else:
		maxRow = len(row)
		for x in range(maxRow):
			if (user_rfc==row[x][7]):
				typeRFC = "Emisor"
				data["Emisor"].append({'Tipo':typeRFC,'cfdi_index_FechaTimbrado': row[x][0],'cfdi_index_FormaPago':row[x][1],'cfdi_index_SubTotal':row[x][2],'cfdi_index_Moneda':row[x][3],'cfdi_index_Total':row[x][4],'cfdi_index_TipoDeComprobante':row[x][5],'cfdi_index_MetodoPago':row[x][6],'cfdi_index_Emisor_Rfc':row[x][7],'cfdi_index_Emisor_Nombre':row[x][8],'cfdi_index_Receptor_Rfc':row[x][9],'cfdi_index_Receptor_Nombre':row[x][10],'cfdi_index_SelloSAT':row[x][11],'cfdi_index_source':row[x][12]})
			else:
				typeRFC = "Receptor"
				data["Receptor"].append({'Tipo':typeRFC,'cfdi_index_FechaTimbrado': row[x][0],'cfdi_index_FormaPago':row[x][1],'cfdi_index_SubTotal':row[x][2],'cfdi_index_Moneda':row[x][3],'cfdi_index_Total':row[x][4],'cfdi_index_TipoDeComprobante':row[x][5],'cfdi_index_MetodoPago':row[x][6],'cfdi_index_Emisor_Rfc':row[x][7],'cfdi_index_Emisor_Nombre':row[x][8],'cfdi_index_Receptor_Rfc':row[x][9],'cfdi_index_Receptor_Nombre':row[x][10],'cfdi_index_SelloSAT':row[x][11],'cfdi_index_source':row[x][12]})
			
	return data


def searchPolizaC(request,date,user_rfc):
	data = []
	cursor = connections['default'].cursor()
	cursor.execute("SELECT poliza_id,user_rfc, poliza_date_search, file_id,poliza_date_created  from cfdi_poliza WHERE  poliza_date_search LIKE '%"+date+"%' AND user_rfc='"+user_rfc+"'")
	row = cursor.fetchall()
	if row is None:
		data = None
	else:
		maxRow = len(row)
		for x in range(maxRow):
			poliza_url = str(request.META.get('HTTP_HOST')) + '/descarga/details/poliza?poliza_id='+ str(row[x][0])
			data.append({'poliza_id':row[x][0],'poliza_details': poliza_url,'user_rfc': row[x][1],'poliza_date_search':row[x][2],'file_id':row[x][3], 'poliza_date_created':row[x][4]})
	return data

def getUserRfc(user_id,user_rfc):
	data = []
	cursor = connections['default'].cursor()
	cursor.execute("SELECT tuf.user_rfc_id,tuf.user_rfc,tuf.user_rfc_location_key,tuf.user_rfc_location_cer  from api_tb_users_rfc tuf WHERE (tuf.user_rfc_estado != 'desactivado' OR tuf.user_rfc_estado IS NULL ) AND tuf.user_id=%s AND tuf.user_rfc=%s",[user_id,user_rfc])
	row = cursor.fetchall()
	if row is None:
		data = None
	else:
		maxRow = len(row)
		for x in range(maxRow):
			data.append({'user_rfc_id': row[x][0],'user_rfc':row[x][1],'user_rfc_location_key':row[x][2],'user_rfc_location_cer':row[x][3]})
	return data

def insertaTemplate(user_rfc,template_name,template_content):
	cursor = connections['default'].cursor()
	cursor.execute("INSERT INTO api_tb_templates(user_rfc,template_name,template_content) VALUES(%s,%s,%s)",[user_rfc,template_name,template_content])
	try:
		currentId = cursor.lastrowid
		row = True
		data = currentId
	except:
		row = "error"
		data = None	

	return data

def templatesByRFC(user_rfc):
	data = []
	cursor = connections['default'].cursor()
	cursor.execute("SELECT template_name,template_content,user_rfc  from api_tb_templates WHERE user_rfc=%s",[user_rfc])
	row = cursor.fetchall()
	if row is None:
		data = row
	else:
		maxRow = len(row)
		for x in range(maxRow):
			data.append({'template_name':row[x][0],'template_content': row[x][1],'user_rfc':row[x][2]})
	return data