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

    def do_Log(self, uuid_sat, uuid_poliza, diferencia, nivel, id_comparacion, fuente):

        logDato = Diferencias(
            field_sat=uuid_sat,
            field_poliza=uuid_poliza,
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

        uuid_found_s = 0
        uuid_found_p = 0
        uuid_found_s_p = 0
        uuid_not_found_s_p = 0
        uuid_found_p_s = 0
        uuid_not_found_p_s = 0

        folio_found_s = 0
        folio_found_p = 0
        folio_found_s_p = 0
        folio_not_found_s_p = 0
        folio_found_p_s = 0
        folio_not_found_p_s = 0

        total_found_s = 0
        total_found_p = 0
        total_found_s_p = 0
        total_found_p_s = 0
        total_not_found_s_p = 0
        total_not_found_p_s = 0

        subtotal_found_s = 0
        subtotal_found_p = 0
        subtotal_found_s_p = 0
        subtotal_found_p_s = 0
        subtotal_not_found_s_p = 0
        subtotal_not_found_p_s = 0

        iva_found_s = 0
        iva_found_p = 0
        iva_found_s_p = 0
        iva_found_p_s = 0
        iva_not_found_s_p = 0
        iva_not_found_p_s = 0

        rfcemisor_found_s = 0
        rfcemisor_found_p = 0
        rfcemisor_found_s_p = 0
        rfcemisor_found_p_s = 0
        rfcemisor_not_found_s_p = 0
        rfcemisor_not_found_p_s = 0

        rfcreceptor_found_s = 0
        rfcreceptor_found_p = 0
        rfcreceptor_found_s_p = 0
        rfcreceptor_found_p_s = 0
        rfcreceptor_not_found_s_p = 0
        rfcreceptor_not_found_p_s = 0

        nombreemisor_found_s = 0
        nombreemisor_found_p = 0
        nombreemisor_found_s_p = 0
        nombreemisor_found_p_s = 0
        nombreemisor_not_found_s_p = 0
        nombreemisor_not_found_p_s = 0

        nombrereceptor_found_s = 0
        nombrereceptor_found_p = 0
        nombrereceptor_found_s_p = 0
        nombrereceptor_found_p_s = 0
        nombrereceptor_not_found_s_p = 0
        nombrereceptor_not_found_p_s = 0

        if datos_sat:
            #uuid and folio
            for data_s in datos_sat:
                print('data_s')
                print(data_s)
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

                            if len(data_p.TIMBRE_UUID) == 0:
                                uuid_found_p = 0
                            else:
                                uuid_found_p = 1

                            if uuid_found_s == 1 and uuid_found_p == 1:
                                if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                    #existe coincide
                                    uuid_found_s_p = uuid_found_s_p + 1
                                else:
                                    #existe no coincide
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'UUID', 'UUID/Folio',objComparar,source)
                            elif uuid_found_s == 1 and uuid_found_p == 0:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'UUID', 'UUID/Folio',objComparar,source)
                            elif uuid_found_s == 0 and uuid_found_p == 1:
                                uuid_not_found_s_p = uuid_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'UUID', 'UUID/Folio',objComparar,source)


                            # print(comparación folio)
                            if len(data_s.folio) == 0:
                                folio_found_s = 0
                            else:
                                folio_found_s = 1

                            if len(data_p.NO_FACTURA) == 0:
                                folio_found_p = 0
                            else:
                                folio_found_p = 1

                            if folio_found_s == 1 and folio_found_p == 1:
                                if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                    # existe coincide
                                    folio_found_s_p = folio_found_s_p + 1
                                else:
                                    # existe no coincide
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'Folio', 'UUID/Folio',objComparar,source)
                            elif folio_found_s == 1 and folio_found_p == 0:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'Folio', 'UUID/Folio',objComparar,source)
                            elif folio_found_s == 0 and folio_found_p == 1:
                                folio_not_found_s_p = folio_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'Folio', 'UUID/Folio',objComparar,source)


                            # print(comparación subtotal, iva, total)
                            # 'subtotal',   'total','total_impuesto_trasladado',
                            #  SUBTOTAL,   TOTAL, IVA,
                            if len(data_s.subtotal) == 0:
                                subtotal_found_s = 0
                            else:
                                subtotal_found_s = 1

                            if len(data_p.SUBTOTAL) == 0:
                                subtotal_found_p = 0
                            else:
                                subtotal_found_p = 1

                            if subtotal_found_s == 1 and subtotal_found_p == 1:
                                if data_s.subtotal == data_p.SUBTOTAL:
                                    # existe coincide
                                    subtotal_found_s_p = subtotal_found_s_p + 1
                                else:
                                    # existe no coincide
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'Sub Total', 'UUID/Folio',objComparar,source)
                            elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'Sub Total', 'UUID/Folio',objComparar,source)
                            elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                self.do_Log(data_s, data_p, 'Sub Total', 'UUID/Folio',objComparar,source)

                            #total
                            if len(data_s.total) == 0:
                                total_found_s = 0
                            else:
                                total_found_s = 1

                            if len(data_p.TOTAL) == 0:
                                total_found_p = 0
                            else:
                                total_found_p = 1

                            if total_found_s == 1 and total_found_p == 1:
                                if data_s.total == data_p.TOTAL:
                                    # existe coincide
                                    total_found_s_p = total_found_s_p + 1
                                else:
                                    # existe no coincide
                                    total_not_found_s_p = total_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'Total', 'UUID/Folio',objComparar,source)
                            elif total_found_s == 1 and total_found_p == 0:
                                self.do_Log(data_s, data_p, 'Total', 'UUID/Folio',objComparar,source)
                                total_not_found_s_p = total_not_found_s_p + 1
                            elif total_found_s == 0 and total_found_p == 1:
                                self.do_Log(data_s, data_p, 'Total', 'UUID/Folio',objComparar,source)
                                total_not_found_s_p = total_not_found_s_p + 1

                            # total_impuesto_trasladado
                            if len(data_s.total_impuesto_trasladado) == 0:
                                iva_found_s = 0
                            else:
                                iva_found_s = 1

                            if len(data_p.IVA) == 0:
                                iva_found_p = 0
                            else:
                                iva_found_p = 1

                            if iva_found_s == 1 and iva_found_p == 1:
                                if data_s.total_impuesto_trasladado == data_p.IVA:
                                    # existe coincide
                                    iva_found_s_p = iva_found_s_p + 1
                                else:
                                    # existe no coincide
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'IVA', 'UUID/Folio',objComparar,source)
                            elif iva_found_s == 1 and iva_found_p == 0:
                                self.do_Log(data_s, data_p, 'IVA', 'UUID/Folio',objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1
                            elif iva_found_s == 0 and iva_found_p == 1:
                                self.do_Log(data_s, data_p, 'IVA', 'UUID/Folio',objComparar,source)
                                iva_not_found_s_p = iva_not_found_s_p + 1

                            #  emisor
                            # 'emisornombre','emisorrfc'
                            #  NOMBRE_EMISOR, RFC_EMISOR
                            if len(data_s.emisornombre) == 0:
                                nombreemisor_found_s = 0
                            else:
                                nombreemisor_found_s = 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombreemisor_found_p = 0
                            else:
                                nombreemisor_found_p = 1

                            if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                    # existe coincide
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                else:
                                    # existe no coincide
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'Nombre Emisor', 'UUID/Folio',objComparar,source)
                            elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, 'Nombre Emisor', 'UUID/Folio',objComparar,source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                self.do_Log(data_s, data_p, 'Nombre Emisor', 'UUID/Folio',objComparar,source)
                                nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                            elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                self.do_Log(data_s, data_p, 'Nombre Emisor (sin valor)', 'UUID/Folio',objComparar,source)
                                nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                            #rfc emisor
                            if len(data_s.emisorrfc) == 0:
                                rfcemisor_found_s = 0
                            else:
                                rfcemisor_found_s = 1

                            if len(data_p.RFC_EMISOR) == 0:
                                rfcemisor_found_p = 0
                            else:
                                rfcemisor_found_p = 1

                            if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                if data_s.emisorrfc == data_p.RFC_EMISOR:
                                    # existe coincide
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                else:
                                    # existe no coincide
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'RFC Emisor', 'UUID/Folio',objComparar,source)
                            elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, 'RFC Emisor', 'UUID/Folio',objComparar,source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                self.do_Log(data_s, data_p, 'RFC Emisor', 'UUID/Folio',objComparar,source)
                                rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                            elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                self.do_Log(data_s, data_p, 'RFC Emisor (sin valor)', 'UUID/Folio',objComparar,source)
                                rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                            # receptor
                            #'receptornombre','receptorrfc'
                            #NOMBRE_RECEPTOR, RFC_RECEPTOR,
                            if len(data_s.receptornombre) == 0:
                                nombrereceptor_found_s = 0
                            else:
                                nombrereceptor_found_s = 1

                            if len(data_p.NOMBRE_EMISOR) == 0:
                                nombrereceptor_found_p = 0
                            else:
                                nombrereceptor_found_p = 1

                            if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                    # existe coincide
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                else:
                                    # existe no coincide
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'Nombre Receptor', 'UUID/Folio',objComparar,source)
                            elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, 'Nombre Receptor', 'UUID/Folio',objComparar,source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                self.do_Log(data_s, data_p, 'Nombre Receptor', 'UUID/Folio',objComparar,source)
                                nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                            elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                self.do_Log(data_s, data_p, 'Nombre Receptor (sin valor)', 'UUID/Folio',objComparar,source)
                                nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                            # rfc receptor
                            if len(data_s.receptorrfc) == 0:
                                rfcreceptor_found_s = 0
                            else:
                                rfcreceptor_found_s = 1

                            if len(data_p.RFC_RECEPTOR) == 0:
                                rfcreceptor_found_p = 0
                            else:
                                rfcreceptor_found_p = 1

                            if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                    # existe coincide
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                else:
                                    # existe no coincide
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, 'RFC Receptor', 'UUID/Folio',objComparar,source)
                            elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, 'RFC Receptor', 'UUID/Folio',objComparar,source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                self.do_Log(data_s, data_p, 'RFC Receptor', 'UUID/Folio',objComparar,source)
                                rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                            elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                self.do_Log(data_s, data_p, 'RFC Receptor (sin valor)', 'UUID/Folio',objComparar,source)
                                rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                else:
                    #not found uuid folio
                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                    self.do_Log(data_s, None, 'UUID, Folio', 'UUID/Folio', objComparar,source)


                #segunda comparación solo UUID
                data_p = DatosPoliza.objects.values('TIMBRE_UUID', 'NO_FACTURA', 'NOMBRE_EMISOR',
                                                    'RFC_EMISOR', 'NOMBRE_RECEPTOR', 'RFC_RECEPTOR',
                                                    'SUBTOTAL', 'TOTAL', 'IVA', 'FECHA_EMISION',  # 'ESTATUS'
                                                    ).filter(identificador_archivo=id_file_p, TIMBRE_UUID=data_s.uuid,
                                                              )
                #tercera comparación solo Folio
                data_p = DatosPoliza.objects.filter(identificador_archivo=id_file_p, NO_FACTURA=data_s.folio)

            for data in datos_poliza:
                source = 'POLIZA'
                total_registros_poliza = len(datos_poliza)
                print(data.TIMBRE_UUID)
                uuid_in_sat = DatosArchivo.objects.filter(identificador_pkt=id_file_s, uuid=data.TIMBRE_UUID)
                print(uuid_in_sat)
                if uuid_in_sat:
                    print("OK")
                    uuid_found_p_s = uuid_found_p_s + 1
                else:
                    print("NOT FOUND")
                    uuid_not_found_p_s = uuid_not_found_p_s + 1

                    print(data.TIMBRE_UUID)
                    self.do_Log(None, data, 'UUID', 'UUID/Folio', objComparar, source)


        cifras = CifrasComparacion(
            archivos_comparados=objComparar,
            total_UUID_sat=uuid_found_s,
            total_UUID_poliza=uuid_found_p,
            total_UUID_sat_poliza=uuid_found_s_p,
            total_UUID_sat_no_poliza=uuid_not_found_s_p,
            total_UUID_poliza_sat=uuid_found_p_s,
            total_UUID_poliza_no_sat=uuid_not_found_p_s,
            total_folio_sat=folio_found_s,
            total_folio_poliza=folio_found_p ,
            total_folio_sat_poliza=folio_found_s_p,
            total_folio_sat_no_poliza=folio_not_found_s_p,
            total_folio_poliza_sat=folio_found_p_s,
            total_folio_poliza_no_sat=folio_not_found_p_s,
            total_total_sat=total_found_s,
            total_total_poliza=total_found_p,
            total_total_sat_poliza=total_found_s_p,
            total_total_sat_no_poliza=total_not_found_s_p,
            total_total_poliza_sat=total_found_p_s,
            total_total_poliza_no_sat=total_not_found_p_s,
            total_subtotal_sat=subtotal_found_s,
            total_subtotal_poliza=subtotal_found_p,
            total_subtotal_sat_poliza=subtotal_found_s_p,
            total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
            total_subtotal_poliza_sat=subtotal_found_p_s,
            total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
            total_iva_sat=iva_found_s,
            total_iva_poliza=iva_found_p,
            total_iva_sat_poliza=iva_found_s_p,
            total_iva_sat_no_poliza=iva_not_found_s_p,
            total_iva_poliza_sat=iva_found_p_s,
            total_iva_poliza_no_sat=iva_not_found_p_s,
            total_rfcemisor_sat=rfcemisor_found_s,
            total_rfcemisor_poliza=rfcemisor_found_p,
            total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
            total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
            total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
            total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
            total_rfcreceptor_sat=rfcreceptor_found_s,
            total_rfcreceptor_poliza=rfcreceptor_found_p,
            total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
            total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
            total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
            total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
            total_nombreemisor_sat=nombreemisor_found_s,
            total_nombreemisor_poliza=nombreemisor_found_p,
            total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
            total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
            total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
            total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
            total_nombrereceptor_sat=nombrereceptor_found_s,
            total_nombrereceptor_poliza=nombrereceptor_found_p,
            total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
            total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
            total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
            total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
            fecha_proceso=gmtime(),
        )
        cifras.save()
        objComparar.total_registros_sat = total_registros_sat
        objComparar.total_registros_poliza = total_registros_poliza
        objComparar.save(update_fields=['total_registros_sat','total_registros_poliza'])


class DiferenciasAdmin(admin.ModelAdmin):
    list_display = ('field_sat','field_poliza','diferencia','nivel_comparacion','comparacion', )
    search_fields = ('field_sat','field_poliza','diferencia','nivel_comparacion','comparacion', )

class CifrasComparacionAdmin(admin.ModelAdmin):
    list_display = ('archivos_comparados','fecha_proceso',)
    search_fields = ('archivos_comparados','fecha_proceso',)


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
