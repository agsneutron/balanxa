from django.contrib import admin

# Register your models here.
from Proceso.models import Procesa, DatosArchivo, DatosLog, PolizaArchivo, DatosPoliza, DatosPolizaLog, ConteoPolizaLog, CompararArchivos, Diferencias, CifrasComparacion
from xml.dom import minidom
import zipfile
import pandas as pnd
from time import gmtime, strftime


class ProcesaAdmin(admin.ModelAdmin):
    list_display = ('archivo',)  #'uuid', 'folio', 'emisorrfc', 'receptorrfc', 'archivo',)


    def do_Log(self, atr, idn, pkt):

        logDato = DatosLog(
            atributo=atr,
            identificador_archivo=idn,
            identificador_pkt=pkt,
        )
        logDato.save()

    def save_model(self, request, obj, form, change):

        super(ProcesaAdmin, self).save_model(request, obj, form, change)

        zf = zipfile.ZipFile(obj.archivo, 'r')
        s_pkt = ''

        s_pkt = zf.filename
        for name in zf.namelist():
            s_folio = ''
            s_uuid = ''
            s_subtotal = ''
            s_total = ''
            s_emisornombre = ''
            s_emisorrfc = ''
            s_receptornombre = ''
            s_receptorrfc = ''
            s_identificador = ''
            s_fechaemision = ''
            s_trasladado = ''

            if not name.startswith('__MACOSX/'):
                f = zf.open(name)
                print('FileName to process:')
                print(f.name)

                s_identificador = f.name

                xmlfile = minidom.parse(f)

                # getItem  folio, totales
                items = xmlfile.getElementsByTagName('cfdi:Comprobante')
                # all item attributes
                print('\nComprobante attributes:')
                for item in items:
                    if item.hasAttribute('Folio'):
                        print(item.attributes['Folio'].value)
                        s_folio = item.attributes['Folio'].value
                    else:
                        self.do_Log('Folio', s_identificador, s_pkt)

                    if item.hasAttribute('SubTotal'):
                        print(item.attributes['SubTotal'].value)
                        s_subtotal = item.attributes['SubTotal'].value
                    else:
                        self.do_Log('SubTotal', s_identificador, s_pkt)

                    if item.hasAttribute('Total'):
                        print(item.attributes['Total'].value)
                        s_total = item.attributes['Total'].value
                    else:
                        self.do_Log('Total', s_identificador, s_pkt)

                # getItem  impuestos trasladados
                items = xmlfile.getElementsByTagName('cfdi:Impuestos')
                # all item attributes
                print('\nImpuestos attributes:')
                for item in items:
                    if item.hasAttribute('TotalImpuestosTrasladados'):
                        print(item.attributes['TotalImpuestosTrasladados'].value)
                        s_trasladado = item.attributes['TotalImpuestosTrasladados'].value
                    else:
                        self.do_Log('TotalImpuestosTrasladados', s_identificador, s_pkt)


                # getItem  rfc emisor, nombre emisor,
                items = xmlfile.getElementsByTagName('cfdi:Emisor')
                # all item attributes
                print('\nEmisor attributes:')
                for item in items:

                    if item.hasAttribute('Rfc'):
                        print(item.attributes['Rfc'].value)
                        s_emisorrfc = item.attributes['Rfc'].value
                    else:
                        self.do_Log('Rfc Emisor', s_identificador, s_pkt)

                    if item.hasAttribute('Nombre'):
                        s_emisornombre = item.attributes['Nombre'].value
                        print(item.attributes['Nombre'].value)
                    else:
                        self.do_Log('Nombre Emisor', s_identificador, s_pkt)

                # getItem  rfc emisor, nombre emisor,
                items = xmlfile.getElementsByTagName('cfdi:Receptor')
                # all item attributes
                print('\nReceptor attributes:')
                for item in items:

                    if item.hasAttribute('Rfc'):
                        s_receptorrfc = item.attributes['Rfc'].value
                        print(item.attributes['Rfc'].value)
                    else:
                        self.do_Log('Rfc Receptor', s_identificador, s_pkt)

                    if item.hasAttribute('Nombre'):
                        print(item.attributes['Nombre'].value)
                        s_receptornombre = item.attributes['Nombre'].value
                    else:
                        self.do_Log('Nombre Receptor', s_identificador, s_pkt)

                # getItem uuid, fecha de emision
                items = xmlfile.getElementsByTagName('tfd:TimbreFiscalDigital')
                # all item attributes
                print('\nTimbreFiscalDigital attributes:')
                for item in items:

                    if item.hasAttribute('FechaTimbrado'):
                        print(item.attributes['FechaTimbrado'].value)
                        s_fechaemision = item.attributes['FechaTimbrado'].value
                    else:
                        self.do_Log('FechaTimbrado', s_identificador, s_pkt)

                    if item.hasAttribute('UUID'):
                        print(item.attributes['UUID'].value)
                        s_uuid = item.attributes['UUID'].value
                    else:
                        self.do_Log('UUID', s_identificador, s_pkt)

                files_data = DatosArchivo(
                    identificador_archivo=s_identificador,
                    identificador_pkt=obj,
                    uuid=s_uuid,
                    folio=s_folio,
                    emisornombre=s_emisornombre,
                    emisorrfc=s_emisorrfc,
                    receptornombre=s_receptornombre,
                    receptorrfc=s_receptorrfc,
                    subtotal=s_subtotal,
                    total=s_total,
                    total_impuesto_trasladado=s_trasladado,
                    fechaemision=s_fechaemision,
                    estatus='',
                )
                files_data.save()




class DatosArchivoAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'folio', 'emisorrfc', 'receptorrfc', 'identificador_archivo', 'identificador_pkt')

    # fieldsets = (
    #    ("Datos del Archivo", {
    #        'fields': ('archivo', 'uuid', 'folio', 'emisorrfc', 'emisornombre', 'receptorrfc', 'receptornombre', 'subtotal', 'total', 'fechaemision', 'estatus' ),
    #    }),
    # )

    readonly_fields = ('uuid', 'folio', 'emisorrfc', 'emisornombre', 'receptorrfc', 'receptornombre', 'subtotal', 'total', 'fechaemision', 'estatus')
    search_fields = ('uuid', 'folio', 'emisorrfc', 'receptorrfc', 'identificador_archivo', 'identificador_pkt')


class DatosLogdmin(admin.ModelAdmin):
    list_display = ('atributo', 'identificador_archivo', 'identificador_pkt')
    search_fields = ('atributo', 'identificador_archivo', 'identificador_pkt')


class PolizaArchivoAdmin(admin.ModelAdmin):
    list_display = ('archivo','fecha', )  #'uuid', 'folio', 'emisorrfc', 'receptorrfc', 'archivo',)

    def do_Log(self, atr, idn, pkt):

        logDato = DatosPolizaLog(
            atributo=atr,
            identificador_archivo=idn,
            identificador_pkt=pkt,
        )
        logDato.save()

    def save_model(self, request, obj, form, change):

        super(PolizaArchivoAdmin, self).save_model(request, obj, form, change)

        ef = pnd.read_excel(obj.archivo, usecols=['NO_FACTURA','SERIE','NOMBRE_RECEPTOR','RFC_RECEPTOR','NOMBRE_EMISOR','RFC_EMISOR',
                                                  'FORMA_PAGO','FECHA_EMISION','TIPO_FACTURA','TIPO_MONEDA','SUBTOTAL','IVA',
                                                  'DESCUENTO','TOTAL','SALDO','FECHA_CREO_XML','TIMBRE_UUID','METODO_PAGO','ESTATUS'])
        s_ef = ''
        #print(ef)
        #print('Dict Data:', ef.to_dict(orient='record'))
        data = ef.to_dict(orient='record')
        s_ef = obj.archivo.name
        print(s_ef)

        s_NO_FACTURA = ''
        s_SERIE = ''
        s_NOMBRE_RECEPTOR = ''
        s_RFC_RECEPTOR = ''
        s_NOMBRE_EMISOR = ''
        s_RFC_EMISOR = ''
        s_FORMA_PAGO = ''
        s_FECHA_EMISION = ''
        s_TIPO_FACTURA = ''
        s_TIPO_MONEDA = ''
        s_SUBTOTAL = ''
        s_IVA = ''
        s_DESCUENTO = ''
        s_TOTAL = ''
        s_SALDO = ''
        s_FECHA_CREO_XML = ''
        s_TIMBRE_UUID = ''
        s_METODO_PAGO = ''
        s_ESTATUS = ''

        for line in data:

            print(line)
            if "NO_FACTURA" in line:
                s_NO_FACTURA = line["NO_FACTURA"]
            else:
                self.do_Log("NO_FACTURA", s_ef, "")

            if "SERIE" in line:
                s_SERIE = line["SERIE"]
            else:
                self.do_Log("SERIE", s_ef, "")

            if "NOMBRE_RECEPTOR" in line:
                s_NOMBRE_RECEPTOR = line["NOMBRE_RECEPTOR"]
            else:
                self.do_Log("NOMBRE_RECEPTOR", s_ef, "")

            if "RFC_RECEPTOR" in line:
                s_RFC_RECEPTOR = line["RFC_RECEPTOR"]
            else:
                self.do_Log("RFC_RECEPTOR", s_ef, "")

            if "NOMBRE_EMISOR" in line:
                s_NOMBRE_EMISOR = line["NOMBRE_EMISOR"]
            else:
                self.do_Log("NOMBRE_EMISOR", s_ef, "")

            if "RFC_EMISOR" in line:
                s_RFC_EMISOR = line["RFC_EMISOR"]
            else:
                self.do_Log("RFC_EMISOR", s_ef, "")

            if "FORMA_PAGO" in line:
                s_FORMA_PAGO = line["FORMA_PAGO"]
            else:
                self.do_Log("FORMA_PAGO", s_ef, "")

            if "FECHA_EMISION" in line:
                s_FECHA_EMISION = line["FECHA_EMISION"]
            else:
                self.do_Log("FECHA_EMISION", s_ef, "")

            if "TIPO_FACTURA" in line:
                s_TIPO_FACTURA = line["TIPO_FACTURA"]
            else:
                self.do_Log("TIPO_FACTURA", s_ef, "")

            if "TIPO_MONEDA" in line:
                s_TIPO_MONEDA = line["TIPO_MONEDA"]
            else:
                self.do_Log("TIPO_MONEDA", s_ef, "")

            if "SUBTOTAL" in line:
                s_SUBTOTAL = line["SUBTOTAL"]
            else:
                self.do_Log("SUBTOTAL", s_ef, "")

            if "IVA" in line:
                s_IVA = line["IVA"]
            else:
                self.do_Log("IVA", s_ef, "")

            if "DESCUENTO" in line:
                s_DESCUENTO = line["DESCUENTO"]
            else:
                self.do_Log("DESCUENTO", s_ef, "")

            if "TOTAL" in line:
                s_TOTAL = line["TOTAL"]
            else:
                self.do_Log("TOTAL", s_ef, "")

            if "SALDO" in line:
                s_SALDO = line["SALDO"]
            else:
                self.do_Log("SALDO", s_ef, "")

            if "FECHA_CREO_XML" in line:
                s_FECHA_CREO_XML = line["FECHA_CREO_XML"]
            else:
                self.do_Log("FECHA_CREO_XML", s_ef, "")

            if "TIMBRE_UUID" in line:
                s_TIMBRE_UUID = line["TIMBRE_UUID"]
            else:
                self.do_Log("TIMBRE_UUID", s_ef, "")

            if "METODO_PAGO" in line:
                s_METODO_PAGO = line["METODO_PAGO"]
            else:
                self.do_Log("METODO_PAGO", s_ef, "")

            if "ESTATUS" in line:
                s_ESTATUS = line["ESTATUS"]
            else:
                self.do_Log("ESTATUS", s_ef, "")

            files_data = DatosPoliza(
                identificador_archivo=obj,
                NO_FACTURA=s_NO_FACTURA,
                SERIE=s_SERIE,
                NOMBRE_RECEPTOR=s_NOMBRE_RECEPTOR,
                RFC_RECEPTOR=s_RFC_RECEPTOR,
                NOMBRE_EMISOR=s_NOMBRE_EMISOR,
                RFC_EMISOR=s_RFC_EMISOR,
                FORMA_PAGO=s_FORMA_PAGO,
                FECHA_EMISION=s_FECHA_EMISION,
                TIPO_FACTURA=s_TIPO_FACTURA,
                TIPO_MONEDA=s_TIPO_MONEDA,
                SUBTOTAL=s_SUBTOTAL,
                IVA=s_IVA,
                DESCUENTO=s_DESCUENTO,
                TOTAL=s_TOTAL,
                SALDO=s_SALDO,
                FECHA_CREO_XML=s_FECHA_CREO_XML,
                TIMBRE_UUID=s_TIMBRE_UUID,
                METODO_PAGO=s_METODO_PAGO,
                ESTATUS=s_ESTATUS,
            )
            files_data.save()


class DatosPolizaAdmin(admin.ModelAdmin):
    list_display = ('NO_FACTURA', 'SERIE', 'NOMBRE_RECEPTOR', 'RFC_RECEPTOR', 'NOMBRE_EMISOR', 'RFC_EMISOR', 'FECHA_EMISION', 'ESTATUS')

    # fieldsets = (
    #    ("Datos del Archivo", {
    #        'fields': ('archivo', 'uuid', 'folio', 'emisorrfc', 'emisornombre', 'receptorrfc', 'receptornombre', 'subtotal', 'total', 'fechaemision', 'estatus' ),
    #    }),
    # )

    #readonly_fields = ('uuid', 'folio', 'emisorrfc', 'emisornombre', 'receptorrfc', 'receptornombre', 'subtotal', 'total', 'fechaemision', 'estatus')
    search_fields = ('NO_FACTURA', 'SERIE', 'NOMBRE_RECEPTOR', 'RFC_RECEPTOR', 'NOMBRE_EMISOR', 'RFC_EMISOR', 'FECHA_EMISION', 'ESTATUS')


class DatosPolizaLogAdmin(admin.ModelAdmin):
    list_display = ('identificador_archivo', 'atributo',)
    search_fields = ('identificador_archivo', 'atributo',)


class ConteoPolizaLogAdmin(admin.ModelAdmin):
    list_display = ('archivo', 'total_procesado', 'total_error', 'total_exito', 'fecha', )
    search_fields = ('archivo', 'total_procesado', 'total_error', 'total_exito', 'fecha', )


class CompararArchivosAdmin(admin.ModelAdmin):
    list_display = ('archivo_sat','archivo_poliza', 'fecha_proceso', 'total_registros_sat', 'total_registros_poliza', 'id_key')  #'uuid', 'folio', 'emisorrfc', 'receptorrfc', 'archivo',)
    readonly_fields = ('total_registros_sat', 'total_registros_poliza', 'fecha_proceso', 'id_key')

    def do_Log(self, uuid_sat, uuid_poliza, uuid_sat_value, uuid_poliza_value, diferencia, nivel, id_comparacion, fuente):

        logDato = Diferencias(
            field_sat=uuid_sat,
            field_poliza=uuid_poliza,
            field_sat_value=uuid_sat_value,
            field_poliza_value=uuid_poliza_value,
            diferencia=diferencia,
            nivel_comparacion=nivel,
            source=fuente,
            comparacion=id_comparacion,
        )
        logDato.save()

    def save_model(self, request, obj, form, change):

        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        obj.total_registros_sat = 0
        obj.total_registros_poliza = 0
        id_key = str(obj.archivo_sat.id) + '-' + str(obj.archivo_poliza.id) + '-' + showtime
        obj.idkey = id_key

        super(CompararArchivosAdmin, self).save_model(request, obj, form, change)

        print('SAVE COMPARACION MODEL')
        print(obj)
        objComparar = CompararArchivos.objects.get(pk=obj.id)

        id_file_s = obj.archivo_sat.id
        id_file_p = obj.archivo_poliza.id
        print(id_file_s)
        print(obj.archivo_poliza.archivo.name)
        print(obj.archivo_sat.archivo.name)
        datos_sat = DatosArchivo.objects.filter(identificador_pkt=id_file_s)
        #'estatus' values('uuid','folio','emisornombre', 'emisorrfc','receptornombre','receptorrfc', 'subtotal','total','total_impuesto_trasladado','fechaemision',).
        datos_poliza = DatosPoliza.objects.filter(identificador_archivo=id_file_p)
        #'ESTATUS' values('TIMBRE_UUID', 'NO_FACTURA', 'NOMBRE_EMISOR', 'RFC_EMISOR', 'NOMBRE_RECEPTOR', 'RFC_RECEPTOR','SUBTOTAL', 'TOTAL', 'IVA', 'FECHA_EMISION',).

        source = ''
        total_registros_sat = 0
        total_registros_poliza = 0

        c_uuid_found_s = 0
        c_uuid_found_p = 0
        uuid_found_s = 0
        uuid_found_p = 0
        uuid_found_s_p = 0
        uuid_not_found_s_p = 0
        uuid_found_p_s = 0
        uuid_not_found_p_s = 0

        c_folio_found_s = 0
        c_folio_found_p = 0
        folio_found_s = 0
        folio_found_p = 0
        folio_found_s_p = 0
        folio_not_found_s_p = 0
        folio_found_p_s = 0
        folio_not_found_p_s = 0

        c_total_found_s = 0
        c_total_found_p = 0
        total_found_s = 0
        total_found_p = 0
        total_found_s_p = 0
        total_found_p_s = 0
        total_not_found_s_p = 0
        total_not_found_p_s = 0

        c_subtotal_found_s = 0
        c_subtotal_found_p = 0
        subtotal_found_s = 0
        subtotal_found_p = 0
        subtotal_found_s_p = 0
        subtotal_found_p_s = 0
        subtotal_not_found_s_p = 0
        subtotal_not_found_p_s = 0

        c_iva_found_s = 0
        c_iva_found_p = 0
        iva_found_s = 0
        iva_found_p = 0
        iva_found_s_p = 0
        iva_found_p_s = 0
        iva_not_found_s_p = 0
        iva_not_found_p_s = 0

        c_rfcemisor_found_s = 0
        c_rfcemisor_found_p = 0
        rfcemisor_found_s = 0
        rfcemisor_found_p = 0
        rfcemisor_found_s_p = 0
        rfcemisor_found_p_s = 0
        rfcemisor_not_found_s_p = 0
        rfcemisor_not_found_p_s = 0

        c_rfcreceptor_found_s = 0
        c_rfcreceptor_found_p = 0
        rfcreceptor_found_s = 0
        rfcreceptor_found_p = 0
        rfcreceptor_found_s_p = 0
        rfcreceptor_found_p_s = 0
        rfcreceptor_not_found_s_p = 0
        rfcreceptor_not_found_p_s = 0

        c_nombreemisor_found_s = 0
        c_nombreemisor_found_p = 0
        nombreemisor_found_s = 0
        nombreemisor_found_p = 0
        nombreemisor_found_s_p = 0
        nombreemisor_found_p_s = 0
        nombreemisor_not_found_s_p = 0
        nombreemisor_not_found_p_s = 0

        c_nombrereceptor_found_s = 0
        c_nombrereceptor_found_p = 0
        nombrereceptor_found_s = 0
        nombrereceptor_found_p = 0
        nombrereceptor_found_s_p = 0
        nombrereceptor_found_p_s = 0
        nombrereceptor_not_found_s_p = 0
        nombrereceptor_not_found_p_s = 0

        if datos_sat:
            #uuid and folio
            for data_s in datos_sat:
                source = 'SAT'
                total_registros_sat = len(datos_sat)
                data_pl = datos_poliza.filter(identificador_archivo=id_file_p, TIMBRE_UUID=data_s.uuid, NO_FACTURA=data_s.folio,)
                if data_pl:
                    for data_p in data_pl:
                        print(data_p.TIMBRE_UUID)
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA\
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:   #estatus
                            print('no dif')
                            uuid_found_s_p = uuid_found_s_p + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    #existe coincide
                                    uuid_found_s_p = uuid_found_s_p + 1
                                else:
                                    #existe no coincide, agregar%coincidencia
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_s_p = folio_found_s_p + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',objComparar,source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',objComparar,source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',objComparar,source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',objComparar,source)


                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_s_p = subtotal_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',objComparar,source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',objComparar,source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',objComparar,source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',objComparar,source)

                            #total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_s_p = total_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_s_p = total_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio', objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_s_p = iva_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID/Folio', objComparar,source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID/Folio', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID/Folio', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID/Folio', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID/Folio', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                            #rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID/Folio', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID/Folio', objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID/Folio', objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID/Folio', objComparar, source)
                                rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                            # receptor
                            #'receptornombre','receptorrfc'
                            #NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID/Folio', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID/Folio', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID/Folio', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID/Folio', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID/Folio', objComparar, source)
                                rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                else:
                    #not found uuid folio
                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                    self.do_Log(data_s, None, data_s.uuid + '/' + data_s.folio,'SIN COINCIDENCIAS', 'UUID, Folio', 'UUID/Folio', objComparar,source)

        if datos_poliza:
            for data_p in datos_poliza:
                source = 'POLIZA'
                total_registros_poliza = len(datos_poliza)
                data_st = datos_sat.filter(identificador_pkt=id_file_s, uuid=data_p.TIMBRE_UUID, folio=data_p.NO_FACTURA)
                if data_st:
                    for data_s in data_st:
                        print('data_s')
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                            print('no dif')
                            uuid_found_p_s = uuid_found_p_s + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    # existe coincide
                                    uuid_found_p_s = uuid_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                            objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_p_s = folio_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                            objComparar, source)

                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_p_s = subtotal_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio', objComparar, source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID/Folio',
                                            objComparar, source)

                            # total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_p_s = total_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_p_s = total_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_p_s = iva_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID/Folio', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID/Folio', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID/Folio', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID/Folio', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID/Folio', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID/Folio', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID/Folio', objComparar, source)
                                nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                            # rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID/Folio', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID/Folio', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID/Folio', objComparar, source)
                                rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                            # receptor
                            # 'receptornombre','receptorrfc'
                            # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID/Folio', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID/Folio', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID/Folio', objComparar, source)
                                rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1

                else:
                    # not found uuid folio
                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                    self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.TIMBRE_UUID + '/' + data_p.NO_FACTURA, 'TIMBRE_UUID/NO_FACTURA',  'UUID/Folio', objComparar, source)

        cifras = CifrasComparacion(
            archivos_comparados=objComparar,
            total_UUID_sat=c_uuid_found_s,
            total_UUID_poliza=c_uuid_found_p,
            total_UUID_sat_poliza=uuid_found_s_p,
            total_UUID_sat_no_poliza=uuid_not_found_s_p,
            total_UUID_poliza_sat=uuid_found_p_s,
            total_UUID_poliza_no_sat=uuid_not_found_p_s,
            total_folio_sat=c_folio_found_s,
            total_folio_poliza=c_folio_found_p,
            total_folio_sat_poliza=folio_found_s_p,
            total_folio_sat_no_poliza=folio_not_found_s_p,
            total_folio_poliza_sat=folio_found_p_s,
            total_folio_poliza_no_sat=folio_not_found_p_s,
            total_total_sat=c_total_found_s,
            total_total_poliza=c_total_found_p,
            total_total_sat_poliza=total_found_s_p,
            total_total_sat_no_poliza=total_not_found_s_p,
            total_total_poliza_sat=total_found_p_s,
            total_total_poliza_no_sat=total_not_found_p_s,
            total_subtotal_sat=c_subtotal_found_s,
            total_subtotal_poliza=c_subtotal_found_p,
            total_subtotal_sat_poliza=subtotal_found_s_p,
            total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
            total_subtotal_poliza_sat=subtotal_found_p_s,
            total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
            total_iva_sat=c_iva_found_s,
            total_iva_poliza=c_iva_found_p,
            total_iva_sat_poliza=iva_found_s_p,
            total_iva_sat_no_poliza=iva_not_found_s_p,
            total_iva_poliza_sat=iva_found_p_s,
            total_iva_poliza_no_sat=iva_not_found_p_s,
            total_rfcemisor_sat=c_rfcemisor_found_s,
            total_rfcemisor_poliza=c_rfcemisor_found_p,
            total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
            total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
            total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
            total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
            total_rfcreceptor_sat=c_rfcreceptor_found_s,
            total_rfcreceptor_poliza=c_rfcreceptor_found_p,
            total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
            total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
            total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
            total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
            total_nombreemisor_sat=c_nombreemisor_found_s,
            total_nombreemisor_poliza=c_nombreemisor_found_p,
            total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
            total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
            total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
            total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
            total_nombrereceptor_sat=c_nombrereceptor_found_s,
            total_nombrereceptor_poliza=c_nombrereceptor_found_p,
            total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
            total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
            total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
            total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
            fecha_proceso=gmtime(),
            registro_comparacion='UUID/Folio',
        )
        cifras.save()

        source = ''
        total_registros_sat = 0
        total_registros_poliza = 0

        c_uuid_found_s = 0
        c_uuid_found_p = 0
        uuid_found_s = 0
        uuid_found_p = 0
        uuid_found_s_p = 0
        uuid_not_found_s_p = 0
        uuid_found_p_s = 0
        uuid_not_found_p_s = 0

        c_folio_found_s = 0
        c_folio_found_p = 0
        folio_found_s = 0
        folio_found_p = 0
        folio_found_s_p = 0
        folio_not_found_s_p = 0
        folio_found_p_s = 0
        folio_not_found_p_s = 0

        c_total_found_s = 0
        c_total_found_p = 0
        total_found_s = 0
        total_found_p = 0
        total_found_s_p = 0
        total_found_p_s = 0
        total_not_found_s_p = 0
        total_not_found_p_s = 0

        c_subtotal_found_s = 0
        c_subtotal_found_p = 0
        subtotal_found_s = 0
        subtotal_found_p = 0
        subtotal_found_s_p = 0
        subtotal_found_p_s = 0
        subtotal_not_found_s_p = 0
        subtotal_not_found_p_s = 0

        c_iva_found_s = 0
        c_iva_found_p = 0
        iva_found_s = 0
        iva_found_p = 0
        iva_found_s_p = 0
        iva_found_p_s = 0
        iva_not_found_s_p = 0
        iva_not_found_p_s = 0

        c_rfcemisor_found_s = 0
        c_rfcemisor_found_p = 0
        rfcemisor_found_s = 0
        rfcemisor_found_p = 0
        rfcemisor_found_s_p = 0
        rfcemisor_found_p_s = 0
        rfcemisor_not_found_s_p = 0
        rfcemisor_not_found_p_s = 0

        c_rfcreceptor_found_s = 0
        c_rfcreceptor_found_p = 0
        rfcreceptor_found_s = 0
        rfcreceptor_found_p = 0
        rfcreceptor_found_s_p = 0
        rfcreceptor_found_p_s = 0
        rfcreceptor_not_found_s_p = 0
        rfcreceptor_not_found_p_s = 0

        c_nombreemisor_found_s = 0
        c_nombreemisor_found_p = 0
        nombreemisor_found_s = 0
        nombreemisor_found_p = 0
        nombreemisor_found_s_p = 0
        nombreemisor_found_p_s = 0
        nombreemisor_not_found_s_p = 0
        nombreemisor_not_found_p_s = 0

        c_nombrereceptor_found_s = 0
        c_nombrereceptor_found_p = 0
        nombrereceptor_found_s = 0
        nombrereceptor_found_p = 0
        nombrereceptor_found_s_p = 0
        nombrereceptor_found_p_s = 0
        nombrereceptor_not_found_s_p = 0
        nombrereceptor_not_found_p_s = 0
        
        # segunda comparación
        # sólo
        # UUID
        if datos_sat:
            #uuid 
            for data_s in datos_sat:
                source = 'SAT'
                total_registros_sat = len(datos_sat)
                data_pl = datos_poliza.filter(identificador_archivo=id_file_p, TIMBRE_UUID=data_s.uuid,)
                if data_pl:
                    for data_p in data_pl:
                        print(data_p.TIMBRE_UUID)
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA\
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:   #estatus
                            print('no dif')
                            uuid_found_s_p = uuid_found_s_p + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    #existe coincide
                                    uuid_found_s_p = uuid_found_s_p + 1
                                else:
                                    #existe no coincide, agregar%coincidencia
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_s_p = folio_found_s_p + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',objComparar,source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',objComparar,source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',objComparar,source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',objComparar,source)


                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_s_p = subtotal_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',objComparar,source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',objComparar,source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',objComparar,source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',objComparar,source)

                            #total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_s_p = total_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_s_p = total_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID', objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID', objComparar, source)
                                total_not_found_s_p = total_not_found_s_p + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_s_p = iva_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID', objComparar,source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'UUID', objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor', 'UUID', objComparar, source)
                                nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                            #rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID', objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID', objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'UUID', objComparar, source)
                                rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                            # receptor
                            #'receptornombre','receptorrfc'
                            #NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR, 'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor', 'UUID', objComparar, source)
                                rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                else:
                    #not found uuid
                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                    self.do_Log(data_s, None,data_s.uuid,'SIN COINCIDENCIAS', 'UUID', 'UUID', objComparar,source)

        #segunda UUID
        if datos_poliza:
            for data_p in datos_poliza:
                source = 'POLIZA'
                total_registros_poliza = len(datos_poliza)
                data_st = datos_sat.filter(identificador_pkt=id_file_s, uuid=data_p.TIMBRE_UUID)
                if data_st:
                    for data_s in data_st:
                        print('data_s')
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                            print('no dif')
                            uuid_found_p_s = uuid_found_p_s + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    # existe coincide
                                    uuid_found_p_s = uuid_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                            objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_p_s = folio_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                            objComparar, source)

                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_p_s = subtotal_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID', objComparar, source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                            objComparar, source)

                            # total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_p_s = total_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_p_s = total_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_p_s = iva_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'UUID', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'UUID', objComparar, source)
                                nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                            # rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'UUID', objComparar, source)
                                rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                            # receptor
                            # 'receptornombre','receptorrfc'
                            # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'UUID', objComparar, source)
                                nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'UUID', objComparar, source)
                                rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1

                else:
                    # not found uuid folio
                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                    self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.TIMBRE_UUID, 'UUID', 'UUID', objComparar, source)

        cifras = CifrasComparacion(
            archivos_comparados=objComparar,
            total_UUID_sat=c_uuid_found_s,
            total_UUID_poliza=c_uuid_found_p,
            total_UUID_sat_poliza=uuid_found_s_p,
            total_UUID_sat_no_poliza=uuid_not_found_s_p,
            total_UUID_poliza_sat=uuid_found_p_s,
            total_UUID_poliza_no_sat=uuid_not_found_p_s,
            total_folio_sat=c_folio_found_s,
            total_folio_poliza=c_folio_found_p,
            total_folio_sat_poliza=folio_found_s_p,
            total_folio_sat_no_poliza=folio_not_found_s_p,
            total_folio_poliza_sat=folio_found_p_s,
            total_folio_poliza_no_sat=folio_not_found_p_s,
            total_total_sat=c_total_found_s,
            total_total_poliza=c_total_found_p,
            total_total_sat_poliza=total_found_s_p,
            total_total_sat_no_poliza=total_not_found_s_p,
            total_total_poliza_sat=total_found_p_s,
            total_total_poliza_no_sat=total_not_found_p_s,
            total_subtotal_sat=c_subtotal_found_s,
            total_subtotal_poliza=c_subtotal_found_p,
            total_subtotal_sat_poliza=subtotal_found_s_p,
            total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
            total_subtotal_poliza_sat=subtotal_found_p_s,
            total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
            total_iva_sat=c_iva_found_s,
            total_iva_poliza=c_iva_found_p,
            total_iva_sat_poliza=iva_found_s_p,
            total_iva_sat_no_poliza=iva_not_found_s_p,
            total_iva_poliza_sat=iva_found_p_s,
            total_iva_poliza_no_sat=iva_not_found_p_s,
            total_rfcemisor_sat=c_rfcemisor_found_s,
            total_rfcemisor_poliza=c_rfcemisor_found_p,
            total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
            total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
            total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
            total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
            total_rfcreceptor_sat=c_rfcreceptor_found_s,
            total_rfcreceptor_poliza=c_rfcreceptor_found_p,
            total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
            total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
            total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
            total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
            total_nombreemisor_sat=c_nombreemisor_found_s,
            total_nombreemisor_poliza=c_nombreemisor_found_p,
            total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
            total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
            total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
            total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
            total_nombrereceptor_sat=c_nombrereceptor_found_s,
            total_nombrereceptor_poliza=c_nombrereceptor_found_p,
            total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
            total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
            total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
            total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
            fecha_proceso=gmtime(),
            registro_comparacion='UUID',
        )
        cifras.save()

        source = ''
        total_registros_sat = 0
        total_registros_poliza = 0

        c_uuid_found_s = 0
        c_uuid_found_p = 0
        uuid_found_s = 0
        uuid_found_p = 0
        uuid_found_s_p = 0
        uuid_not_found_s_p = 0
        uuid_found_p_s = 0
        uuid_not_found_p_s = 0

        c_folio_found_s = 0
        c_folio_found_p = 0
        folio_found_s = 0
        folio_found_p = 0
        folio_found_s_p = 0
        folio_not_found_s_p = 0
        folio_found_p_s = 0
        folio_not_found_p_s = 0

        c_total_found_s = 0
        c_total_found_p = 0
        total_found_s = 0
        total_found_p = 0
        total_found_s_p = 0
        total_found_p_s = 0
        total_not_found_s_p = 0
        total_not_found_p_s = 0

        c_subtotal_found_s = 0
        c_subtotal_found_p = 0
        subtotal_found_s = 0
        subtotal_found_p = 0
        subtotal_found_s_p = 0
        subtotal_found_p_s = 0
        subtotal_not_found_s_p = 0
        subtotal_not_found_p_s = 0

        c_iva_found_s = 0
        c_iva_found_p = 0
        iva_found_s = 0
        iva_found_p = 0
        iva_found_s_p = 0
        iva_found_p_s = 0
        iva_not_found_s_p = 0
        iva_not_found_p_s = 0

        c_rfcemisor_found_s = 0
        c_rfcemisor_found_p = 0
        rfcemisor_found_s = 0
        rfcemisor_found_p = 0
        rfcemisor_found_s_p = 0
        rfcemisor_found_p_s = 0
        rfcemisor_not_found_s_p = 0
        rfcemisor_not_found_p_s = 0

        c_rfcreceptor_found_s = 0
        c_rfcreceptor_found_p = 0
        rfcreceptor_found_s = 0
        rfcreceptor_found_p = 0
        rfcreceptor_found_s_p = 0
        rfcreceptor_found_p_s = 0
        rfcreceptor_not_found_s_p = 0
        rfcreceptor_not_found_p_s = 0

        c_nombreemisor_found_s = 0
        c_nombreemisor_found_p = 0
        nombreemisor_found_s = 0
        nombreemisor_found_p = 0
        nombreemisor_found_s_p = 0
        nombreemisor_found_p_s = 0
        nombreemisor_not_found_s_p = 0
        nombreemisor_not_found_p_s = 0

        c_nombrereceptor_found_s = 0
        c_nombrereceptor_found_p = 0
        nombrereceptor_found_s = 0
        nombrereceptor_found_p = 0
        nombrereceptor_found_s_p = 0
        nombrereceptor_found_p_s = 0
        nombrereceptor_not_found_s_p = 0
        nombrereceptor_not_found_p_s = 0

        # tercera comparación
        # sólo
        # Folio
        if datos_sat:
            # folio
            for data_s in datos_sat:
                source = 'SAT'
                total_registros_sat = len(datos_sat)
                data_pl = datos_poliza.filter(identificador_archivo=id_file_p, NO_FACTURA=data_s.folio, )
                if data_pl:
                    for data_p in data_pl:
                        print(data_p.TIMBRE_UUID)
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                            print('no dif')
                            uuid_found_s_p = uuid_found_s_p + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    # existe coincide
                                    uuid_found_s_p = uuid_found_s_p + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_s_p = folio_found_s_p + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)

                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_s_p = subtotal_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)

                            # total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_s_p = total_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_s_p = total_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO', objComparar,
                                            source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO', objComparar,
                                            source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO', objComparar,
                                            source)
                                total_not_found_s_p = total_not_found_s_p + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_s_p = iva_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO', objComparar, source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'FOLIO',
                                            objComparar, source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'FOLIO',
                                            objComparar, source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA', 'FOLIO',
                                            objComparar, source)
                                iva_not_found_s_p = iva_not_found_s_p + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'FOLIO', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                            # rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'FOLIO',
                                            objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'FOLIO',
                                            objComparar, source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor', 'FOLIO',
                                            objComparar, source)
                                rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                            # receptor
                            # 'receptornombre','receptorrfc'
                            # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                else:
                    # not found uuid folio
                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                    self.do_Log(data_s, None, data_s.uuid, 'SIN COINCIDENCIAS', 'UUID', 'FOLIO', objComparar, source)

        #tercera folio poliza
        if datos_poliza:
            for data_p in datos_poliza:
                source = 'POLIZA'
                total_registros_poliza = len(datos_poliza)
                data_st = datos_sat.filter(identificador_pkt=id_file_s, folio=data_p.NO_FACTURA)
                if data_st:
                    for data_s in data_st:
                        print('data_s')
                        if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                and data_s.emisorrfc == data_p.RFC_EMISOR \
                                and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                and data_s.subtotal == data_p.SUBTOTAL \
                                and data_s.total == data_p.TOTAL \
                                and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                            print('no dif')
                            uuid_found_p_s = uuid_found_p_s + 1
                        else:
                            # print(comparación uuid)
                            if len(data_s.uuid) == 0:
                                uuid_found_s = 0
                            else:
                                uuid_found_s = 1
                                c_uuid_found_s = c_uuid_found_s + 1
                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1
                                c_uuid_found_p = c_uuid_found_p + 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    # existe coincide
                                    uuid_found_p_s = uuid_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)
                            elif uuid_found_s == 0 and uuid_found_p == 0:
                                uuid_not_found_p_s = uuid_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                            objComparar, source)

                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1
                                c_folio_found_s = c_folio_found_s + 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1
                                c_folio_found_p = c_folio_found_p + 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_p_s = folio_found_p_s + 1
                                else:
                                    # existe no coincide, agregar%coincidencia
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)
                            elif folio_found_s == 0 and folio_found_p == 0:
                                folio_not_found_p_s = folio_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                            objComparar, source)

                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1
                                c_subtotal_found_s = c_subtotal_found_s + 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1
                                c_subtotal_found_p = c_subtotal_found_p + 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_p_s = subtotal_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'FOLIO', objComparar, source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                            objComparar, source)

                            # total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1
                                c_total_found_s = c_total_found_s + 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1
                                c_total_found_p = c_total_found_p + 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_p_s = total_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coincidencia
                                    total_not_found_p_s = total_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar, source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1
                            elif total_found_s == 0 and total_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                            objComparar, source)
                                total_not_found_p_s = total_not_found_p_s + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1
                                c_iva_found_s = c_iva_found_s + 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1
                                c_iva_found_p = c_iva_found_p + 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_p_s = iva_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coincidencia
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO', objComparar, source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'FOLIO', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'FOLIO', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1
                            elif iva_found_s == 0 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                            'FOLIO', objComparar, source)
                                iva_not_found_p_s = iva_not_found_p_s + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1
                                c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1
                                c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'FOLIO', objComparar, source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR, 'Nombre Emisor',
                                            'FOLIO', objComparar, source)
                                nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                            # rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1
                                c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1
                                c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO', objComparar, source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'FOLIO', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'FOLIO', objComparar, source)
                                rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                            'FOLIO', objComparar, source)
                                rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                            # receptor
                            # 'receptornombre','receptorrfc'
                            # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1
                                c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1
                                c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                else:
                                    # existe no coincide  agregar%coicidencia
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                            'Nombre Receptor', 'FOLIO', objComparar, source)
                                nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1
                                c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1
                                c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                else:
                                    # existe no coincide agregar%coicidencia
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                            'FOLIO', objComparar, source)
                                rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1

                else:
                    # not found folio
                    folio_not_found_p_s = folio_not_found_p_s + 1
                    self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.NO_FACTURA, 'Folio', 'FOLIO', objComparar, source)

        cifras = CifrasComparacion(
            archivos_comparados=objComparar,
            total_UUID_sat=c_uuid_found_s,
            total_UUID_poliza=c_uuid_found_p,
            total_UUID_sat_poliza=uuid_found_s_p,
            total_UUID_sat_no_poliza=uuid_not_found_s_p,
            total_UUID_poliza_sat=uuid_found_p_s,
            total_UUID_poliza_no_sat=uuid_not_found_p_s,
            total_folio_sat=c_folio_found_s,
            total_folio_poliza=c_folio_found_p,
            total_folio_sat_poliza=folio_found_s_p,
            total_folio_sat_no_poliza=folio_not_found_s_p,
            total_folio_poliza_sat=folio_found_p_s,
            total_folio_poliza_no_sat=folio_not_found_p_s,
            total_total_sat=c_total_found_s,
            total_total_poliza=c_total_found_p,
            total_total_sat_poliza=total_found_s_p,
            total_total_sat_no_poliza=total_not_found_s_p,
            total_total_poliza_sat=total_found_p_s,
            total_total_poliza_no_sat=total_not_found_p_s,
            total_subtotal_sat=c_subtotal_found_s,
            total_subtotal_poliza=c_subtotal_found_p,
            total_subtotal_sat_poliza=subtotal_found_s_p,
            total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
            total_subtotal_poliza_sat=subtotal_found_p_s,
            total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
            total_iva_sat=c_iva_found_s,
            total_iva_poliza=c_iva_found_p,
            total_iva_sat_poliza=iva_found_s_p,
            total_iva_sat_no_poliza=iva_not_found_s_p,
            total_iva_poliza_sat=iva_found_p_s,
            total_iva_poliza_no_sat=iva_not_found_p_s,
            total_rfcemisor_sat=c_rfcemisor_found_s,
            total_rfcemisor_poliza=c_rfcemisor_found_p,
            total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
            total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
            total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
            total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
            total_rfcreceptor_sat=c_rfcreceptor_found_s,
            total_rfcreceptor_poliza=c_rfcreceptor_found_p,
            total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
            total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
            total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
            total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
            total_nombreemisor_sat=c_nombreemisor_found_s,
            total_nombreemisor_poliza=c_nombreemisor_found_p,
            total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
            total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
            total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
            total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
            total_nombrereceptor_sat=c_nombrereceptor_found_s,
            total_nombrereceptor_poliza=c_nombrereceptor_found_p,
            total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
            total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
            total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
            total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
            fecha_proceso=gmtime(),
            registro_comparacion='FOLIO',
        )
        cifras.save()

        objComparar.total_registros_sat = total_registros_sat
        objComparar.total_registros_poliza = total_registros_poliza
        objComparar.save(update_fields=['total_registros_sat','total_registros_poliza'])


class DiferenciasAdmin(admin.ModelAdmin):
    list_display = ('field_sat', 'field_poliza', 'field_sat_value', 'field_poliza_value', 'diferencia', 'nivel_comparacion','source', 'comparacion', )
    search_fields = ('field_sat', 'field_poliza', 'field_sat_value', 'field_poliza_value', 'diferencia', 'nivel_comparacion', 'source', 'comparacion', )


class CifrasComparacionAdmin(admin.ModelAdmin):
    list_display = ('archivos_comparados','registro_comparacion','fecha_proceso',)
    search_fields = ('archivos_comparados','registro_comparacion','fecha_proceso',)


admin.site.register(Procesa, ProcesaAdmin)
admin.site.register(DatosArchivo, DatosArchivoAdmin)
admin.site.register(DatosLog, DatosLogdmin)
admin.site.register(PolizaArchivo, PolizaArchivoAdmin)
admin.site.register(DatosPoliza, DatosPolizaAdmin)
admin.site.register(DatosPolizaLog, DatosPolizaLogAdmin)
admin.site.register(ConteoPolizaLog, ConteoPolizaLogAdmin)
admin.site.register(CompararArchivos, CompararArchivosAdmin)
admin.site.register(Diferencias, DiferenciasAdmin)
admin.site.register(CifrasComparacion,CifrasComparacionAdmin)
