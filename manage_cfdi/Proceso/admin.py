from django.contrib import admin

# Register your models here.
from Proceso.models import Procesa, DatosArchivo, DatosLog, PolizaArchivo, DatosPoliza, DatosPolizaLog, ConteoPolizaLog, Comparar_UUID, DiferenciasUUID
from xml.dom import minidom
import zipfile
import pandas as pnd


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
                    identificador_pkt=s_pkt,
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

        super(ProcesaAdmin, self).save_model(request, obj, form, change)


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


class Comparar_UUIDAdmin(admin.ModelAdmin):
    list_display = ('archivo_sat','archivo_poliza', 'fecha_proceso', 'total_UUID_sat', 'total_UUID_poliza', 'total_sat_no_poliza', 'total_poliza_no_sat')  #'uuid', 'folio', 'emisorrfc', 'receptorrfc', 'archivo',)

    def do_Log(self, uuid_sat, uuid_poliza,id_comparacion):

        logDato = DiferenciasUUID(
            UUID_sat=uuid_sat,
            UUID_poliza=uuid_poliza,
            comparacion=id_comparacion,
        )
        logDato.save()

    def save_model(self, request, obj, form, change):

        print(obj)
        super(Comparar_UUIDAdmin, self).save_model(request, obj, form, change)



admin.site.register(Procesa, ProcesaAdmin)
admin.site.register(DatosArchivo, DatosArchivoAdmin)
admin.site.register(DatosLog, DatosLogdmin)
admin.site.register(PolizaArchivo, PolizaArchivoAdmin)
admin.site.register(DatosPoliza, DatosPolizaAdmin)
admin.site.register(DatosPolizaLog, DatosPolizaLogAdmin)
admin.site.register(ConteoPolizaLog, ConteoPolizaLogAdmin)
admin.site.register(Comparar_UUID, Comparar_UUIDAdmin)