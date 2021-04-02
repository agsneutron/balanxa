
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Empresa(models.Model):
    nombre = models.CharField(verbose_name="Nombre de la Empresa", max_length=200, null=False, blank=True, unique=True)
    membresia = models.BigIntegerField(verbose_name="Membresia", null=False, blank=True, unique=False)
    rfc = models.CharField(verbose_name="RFC de la Empresa", max_length=200, null=False, blank=True, unique=True)


    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):  # __unicode__ on Python 2
        return self.nombre + ' - ' + str(self.rfc)


class Procesa(models.Model):
    #carga archivo SAT .zip
    archivo = models.FileField(verbose_name="Archivo SAT",  null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga", auto_now=True, null=False, blank=False)
    total_registros_procesados = models.BigIntegerField(verbose_name="Total de XML procesados", null=False, unique=False)
    total_registros_error = models.BigIntegerField(verbose_name="Total de XML con error", null=False, unique=False)
    total_registros_correctos = models.BigIntegerField(verbose_name="Total de XML correctos", null=False, unique=False)

    class Meta:
        verbose_name = "Archivo SAT"
        verbose_name_plural = "Archivos SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class DatosArchivo(models.Model):
    #datos obtenidos del XML
    identificador_archivo = models.CharField(verbose_name="Identificador del archivo", max_length=200, null=False, blank=True, unique=False)
    identificador_pkt = models.ForeignKey(Procesa, verbose_name="Identificador del Paquete", on_delete=models.CASCADE, )
    uuid = models.CharField(verbose_name="UUID", max_length=200, null=False, blank=True, unique=False)
    folio = models.CharField(verbose_name="Folio", max_length=200, null=False, blank=True, unique=False)
    rfc = models.CharField(verbose_name="RFC", max_length=200, null=False, blank=True, unique=False)
    emisornombre = models.CharField(verbose_name="Nombre emisor", max_length=200, null=False, blank=True, unique=False)
    emisorrfc = models.CharField(verbose_name="RFC emisor", max_length=200, null=False, blank=True, unique=False)
    receptornombre = models.CharField(verbose_name="Nombre receptor", max_length=200, null=False, blank=True, unique=False)
    receptorrfc = models.CharField(verbose_name="RFC receptor", max_length=200, null=False, blank=True, unique=False)
    subtotal = models.CharField(verbose_name="Subtotal", max_length=200, null=False, blank=True, unique=False)
    total = models.CharField(verbose_name="Total", max_length=200, null=False, blank=True, unique=False)
    total_impuesto_trasladado = models.CharField(verbose_name="Total Impuestos Trasladados", max_length=200, null=False, blank=True, unique=False)
    fechaemision = models.DateTimeField(verbose_name="Fecha de Timbrado", null=False, blank=True, unique=False)
    estatus = models.CharField(verbose_name="Estatus", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Datos de XML en PKT SAT"
        verbose_name_plural = "Datos de XML en PKT SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.identificador_archivo + ' - ' + self.folio


class DatosLog(models.Model):
    #log para registrar los atributos no encontrados en el XML
    identificador_archivo = models.CharField(verbose_name="Identificador del archivo", max_length=200, null=False,
                                             blank=True, unique=False)
    identificador_pkt = models.CharField(verbose_name="Identificador del paquete", max_length=200, null=False,
                                         blank=True, unique=False)
    atributo = models.CharField(verbose_name="Atributo", max_length=200, null=False,
                                         blank=True, unique=False)


    class Meta:
        verbose_name = "Log datos SAT con Error"
        verbose_name_plural = "Log datos SAT con Error"

    def __str__(self):  # __unicode__ on Python 2
        return self.atributo


class PolizaArchivo(models.Model):
    #carga de polizas xlxs
    archivo = models.FileField(verbose_name="Archivo",  null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])])
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)
    total_registros_procesados = models.BigIntegerField(verbose_name="Total de Polizas procesadas", null=False,
                                                        unique=False)
    total_registros_error = models.BigIntegerField(verbose_name="Total de Polizas con error", null=False, unique=False)
    total_registros_correctos = models.BigIntegerField(verbose_name="Total de Polizas correctas", null=False, unique=False)

    class Meta:
        verbose_name = "Archivo de Polizas"
        verbose_name_plural = "Archivos de Polizas"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class DatosPoliza(models.Model):
    #datos obtenidos de los registros del xlsx
    identificador_archivo = models.ForeignKey(PolizaArchivo, verbose_name="Identificador del Archivo", on_delete=models.CASCADE, )
    NO_FACTURA = models.CharField(verbose_name="No. Factura", max_length=200, null=False, blank=True, unique=False)
    SERIE = models.CharField(verbose_name="Serie", max_length=200, null=False, blank=True, unique=False)
    NOMBRE_RECEPTOR = models.CharField(verbose_name="Nombre Rceptor", max_length=200, null=False, blank=True, unique=False)
    RFC_RECEPTOR = models.CharField(verbose_name="RFC Receptor", max_length=200, null=False, blank=True, unique=False)
    NOMBRE_EMISOR = models.CharField(verbose_name="Nombre Emisor", max_length=200, null=False, blank=True, unique=False)
    RFC_EMISOR = models.CharField(verbose_name="RFC Emisor", max_length=200, null=False, blank=True, unique=False)
    FORMA_PAGO = models.CharField(verbose_name="Forma de Pago", max_length=200, null=False, blank=True, unique=False)
    FECHA_EMISION = models.DateTimeField(verbose_name="Fecha de Emmisión", null=False, blank=True, unique=False)
    TIPO_FACTURA = models.CharField(verbose_name="Tipo de Factura", max_length=200, null=False, blank=True, unique=False)
    TIPO_MONEDA = models.CharField(verbose_name="Tipo de Moneda", max_length=200, null=False, blank=True, unique=False)
    SUBTOTAL = models.CharField(verbose_name="Sub Total", max_length=200, null=False, blank=True, unique=False)
    IVA = models.CharField(verbose_name="IVA", max_length=200, null=False, blank=True, unique=False)
    DESCUENTO = models.CharField(verbose_name="Descuento", max_length=200, null=False, blank=True, unique=False)
    TOTAL = models.CharField(verbose_name="Total", max_length=200, null=False, blank=True, unique=False)
    SALDO = models.CharField(verbose_name="Saldo", max_length=200, null=False, blank=True, unique=False)
    FECHA_CREO_XML = models.DateTimeField(verbose_name="Fecha de Creación de XML", null=False, blank=True, unique=False)
    TIMBRE_UUID = models.CharField(verbose_name="Timbre UUID", max_length=200, null=False, blank=True, unique=False)
    METODO_PAGO = models.CharField(verbose_name="Método de Pago", max_length=200, null=False, blank=True, unique=False)
    ESTATUS = models.CharField(verbose_name="Estatus", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Datos de la Poliza"
        verbose_name_plural = "Datos de las Polizas"

    def __str__(self):  # __unicode__ on Python 2
        return self.identificador_archivo.archivo.name + ' - ' + str(self.NO_FACTURA)


class DatosPolizaLog(models.Model):
    #errores encontrados al cargar los registros del XLXS ejm. vacios
    identificador_archivo = models.CharField(verbose_name="Identificador del archivo", max_length=200, null=False,
                                             blank=True, unique=False)
    atributo = models.CharField(verbose_name="Atributo", max_length=200, null=False,
                                         blank=True, unique=False)


    class Meta:
        verbose_name = "Log datos Poliza"
        verbose_name_plural = "Log datos Poliza"

    def __str__(self):  # __unicode__ on Python 2
        return self.atributo


class ConteoPolizaLog(models.Model):
    #conteos de incidencias encontradas por Poliza -- atributos
    archivo = models.ForeignKey(DatosPoliza, verbose_name="Poliza:", null=False, on_delete=models.CASCADE,)
    total_procesado = models.BigIntegerField(verbose_name="Número Factura:", null=False, unique=False)
    total_error = models.BigIntegerField(verbose_name="Total de atributos con error:", null=False, unique=False)
    total_exito = models.BigIntegerField(verbose_name="Total de atributos correctos:", null=False, unique=False)
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Cifras de Registros Procesados POLIZA"
        verbose_name_plural = "Cifras de Registros Procesados POLIZA"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class ConteoXMLLog(models.Model):
    # conteos de incidencias encontradas por XML --- atributos
    archivo = models.ForeignKey(DatosArchivo, verbose_name="Archivo:", null=False, on_delete=models.CASCADE,)
    total_error = models.BigIntegerField(verbose_name="Total de atributos con error:", null=False, unique=False)
    total_exito = models.BigIntegerField(verbose_name="Total de atributos correctos:", null=False, unique=False)
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Cifras de Registros Procesados XML"
        verbose_name_plural = "Cifras de Registros Procesados XML"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class CompararArchivos(models.Model):
    ## comparación de archivo vs archivo
    archivo_sat = models.ForeignKey(Procesa, verbose_name="Archivo SAT:", null=False, on_delete=models.CASCADE)
    archivo_poliza = models.ForeignKey(PolizaArchivo, verbose_name="Archivo Poliza:", null=False, on_delete=models.CASCADE, )
    total_registros_sat = models.BigIntegerField(verbose_name="Total de registros SAT:", null=False, unique=False)
    total_registros_poliza = models.BigIntegerField(verbose_name="Total de registros Poliza:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)
    id_key = models.CharField(verbose_name="Comparación", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Comparación Archivos"
        verbose_name_plural = "Comparaciones Archivos"

    def __str__(self):  # __unicode__ on Python 2
        return self.id_key + '-' + self.archivo_sat.archivo.name + '-' + self.archivo_poliza.archivo.name


class CompararPorFecha(models.Model):
    #comparación fecha vs fecha
    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", null=False, on_delete=models.CASCADE,)
    fecha_inicio = models.DateTimeField(verbose_name="Fecha inicio", null=False, blank=False)
    fecha_fin = models.DateTimeField(verbose_name="Fecha fin",  null=False, blank=False)
    total_registros_sat = models.BigIntegerField(verbose_name="Total de registros SAT", null=False, unique=False)
    total_registros_poliza = models.BigIntegerField(verbose_name="Total de registros Poliza", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de carga", auto_now=True, null=False, blank=False)
    id_key = models.CharField(verbose_name="Comparación", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Comparación de Archivos por Fecha"
        verbose_name_plural = "Comparaciones de Archivos por Fecha"

    def __str__(self):  # __unicode__ on Python 2
        return self.id_key


class CifrasComparacion(models.Model):
    #cifras control de la comparación archivo vs archivo
    archivos_comparados = models.ForeignKey(CompararArchivos, verbose_name="Comparacion:", null=False, on_delete=models.CASCADE, )
    total_UUID_sat = models.BigIntegerField(verbose_name="UUIDs en archivo SAT:", null=False, unique=False)
    total_UUID_poliza = models.BigIntegerField(verbose_name="UUIDs en archivo Poliza:", null=False, unique=False)
    total_UUID_sat_poliza = models.BigIntegerField(verbose_name="UUIDs del SAT en Poliza:", null=False, unique=False)
    total_UUID_poliza_sat = models.BigIntegerField(verbose_name="UUIDs de Poliza en SAT:", null=False, unique=False)
    total_UUID_sat_no_poliza = models.BigIntegerField(verbose_name="UUIDs del SAT no encontrados en Poliza:", null=False, unique=False)
    total_UUID_poliza_no_sat = models.BigIntegerField(verbose_name="UUIDs de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_folio_sat = models.BigIntegerField(verbose_name="Folios en archivo SAT:", null=False, unique=False)
    total_folio_poliza = models.BigIntegerField(verbose_name="Folios en archivo Poliza:", null=False, unique=False)
    total_folio_sat_no_poliza = models.BigIntegerField(verbose_name="Folios del SAT no encontrados en Poliza:", null=False, unique=False)
    total_folio_poliza_no_sat = models.BigIntegerField(verbose_name="Folios de Poliza no encontrados en SAT:", null=False, unique=False)
    total_folio_sat_poliza = models.BigIntegerField(verbose_name="Folios del SAT  en Poliza:", null=False, unique=False)
    total_folio_poliza_sat = models.BigIntegerField(verbose_name="Folios de la  Poliza en SAT:", null=False, unique=False)
    total_total_sat = models.BigIntegerField(verbose_name="Totales en archivo SAT:", null=False, unique=False)
    total_total_poliza = models.BigIntegerField(verbose_name="Totales en archivo Poliza:", null=False, unique=False)
    total_total_sat_no_poliza = models.BigIntegerField(verbose_name="Totales del SAT no encontrados en Poliza:", null=False, unique=False)
    total_total_poliza_no_sat = models.BigIntegerField(verbose_name="Totales de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_total_sat_poliza = models.BigIntegerField(verbose_name="Totales del SAT en Poliza:", null=False, unique=False)
    total_total_poliza_sat = models.BigIntegerField(verbose_name="Totales de la  Poliza en SAT:", null=False, unique=False)
    total_subtotal_sat = models.BigIntegerField(verbose_name="Sub Totales en archivo SAT:", null=False, unique=False)
    total_subtotal_poliza = models.BigIntegerField(verbose_name="Sub Totales en archivo Poliza:", null=False, unique=False)
    total_subtotal_sat_no_poliza = models.BigIntegerField(verbose_name="Sub Totales del SAT no encontrados en Poliza:", null=False, unique=False)
    total_subtotal_poliza_no_sat = models.BigIntegerField(verbose_name="Sub Totales de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_subtotal_sat_poliza = models.BigIntegerField(verbose_name="Sub Totales del SAT en  Poliza:", null=False, unique=False)
    total_subtotal_poliza_sat = models.BigIntegerField(verbose_name="Sub Totales de la Poliza en SAT:", null=False, unique=False)
    total_iva_sat = models.BigIntegerField(verbose_name="IVA en archivo SAT:", null=False, unique=False)
    total_iva_poliza = models.BigIntegerField(verbose_name="IVA en archivo Poliza:", null=False, unique=False)
    total_iva_sat_no_poliza = models.BigIntegerField(verbose_name="IVA del SAT no encontrados en Poliza:", null=False, unique=False)
    total_iva_poliza_no_sat = models.BigIntegerField(verbose_name="IVA de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_iva_sat_poliza = models.BigIntegerField(verbose_name="IVA del SAT en Poliza:", null=False, unique=False)
    total_iva_poliza_sat = models.BigIntegerField(verbose_name="IVA de la Poliza en SAT:", null=False, unique=False)
    total_rfcemisor_sat = models.BigIntegerField(verbose_name="RFCs Emisor en archivo SAT:", null=False, unique=False)
    total_rfcemisor_poliza = models.BigIntegerField(verbose_name="RFCs Emisor en archivo Poliza:", null=False, unique=False)
    total_rfcemisor_sat_no_poliza = models.BigIntegerField(verbose_name="RFCs Emisor del SAT no encontrados en Poliza:", null=False, unique=False)
    total_rfcemisor_poliza_no_sat = models.BigIntegerField(verbose_name="RFCs Emisor de Poliza no encontrados en SAT:", null=False, unique=False)
    total_rfcemisor_sat_poliza = models.BigIntegerField(verbose_name="RFCs Emisor del SAT en Poliza:",  null=False, unique=False)
    total_rfcemisor_poliza_sat = models.BigIntegerField(verbose_name="RFCs Emisor de la Poliza en SAT:", null=False, unique=False)
    total_rfcreceptor_sat = models.BigIntegerField(verbose_name="RFCs Receptor en archivo SAT:", null=False, unique=False)
    total_rfcreceptor_poliza = models.BigIntegerField(verbose_name="RFCs Receptor en archivo Poliza:", null=False, unique=False)
    total_rfcreceptor_sat_no_poliza = models.BigIntegerField(verbose_name="RFC Receptor de SAT no encontrado en Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_no_sat = models.BigIntegerField(verbose_name="RFC Receptor de Poliza no encontrado en SAT:", null=False, unique=False)
    total_rfcreceptor_sat_poliza = models.BigIntegerField(verbose_name="RFCs Receptor del SAT en archivo Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_sat = models.BigIntegerField(verbose_name="RFCs Receptor de la Poliza en SAT:", null=False, unique=False)
    total_nombreemisor_sat = models.BigIntegerField(verbose_name="Nombre Emisor en archivo SAT:", null=False, unique=False)
    total_nombreemisor_poliza = models.BigIntegerField(verbose_name="Nombre Emisor en archivo Poliza:", null=False, unique=False)
    total_nombreemisor_sat_no_poliza = models.BigIntegerField(verbose_name="Nombre Emisor SAT no encontrado en Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_no_sat = models.BigIntegerField(verbose_name="Nombre Emisor Poliza no encontrado en SAT:", null=False, unique=False)
    total_nombreemisor_sat_poliza = models.BigIntegerField(verbose_name="Nombre Emisor  del SAT en Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_sat = models.BigIntegerField(verbose_name="Nombre Emisor de la Poliza en SAT:", null=False, unique=False)
    total_nombrereceptor_sat = models.BigIntegerField(verbose_name="Nombre Receptor en archivo SAT:", null=False, unique=False)
    total_nombrereceptor_poliza = models.BigIntegerField(verbose_name="Nombre Receptor en archivo Poliza:", null=False, unique=False)
    total_nombrereceptor_sat_no_poliza = models.BigIntegerField(verbose_name="NombreReceptor SAT no coincide en Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_no_sat = models.BigIntegerField(verbose_name="NombreReceptor Poliza no coincide en SAT:", null=False, unique=False)
    total_nombrereceptor_sat_poliza = models.BigIntegerField(verbose_name="Nombre Receptor de SAT en  Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_sat = models.BigIntegerField(verbose_name="Nombre Receptor de la  Poliza  en SAT:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de comparación:", auto_now=True, null=False, blank=False)
    registro_comparacion = models.CharField(verbose_name="Registro de Comparación:", null=False, blank=False, max_length=200,)

    class Meta:
        verbose_name = "Cifras de Comparación de Archivos"
        verbose_name_plural = "Cifras de Comparación de Archivos"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivos_comparados.id_key + '-' + self.registro_comparacion


class CifrasComparacionFecha(models.Model):
    #cifras control de la comparación archivo vs archivo
    fechas_comparacion = models.ForeignKey(CompararPorFecha, verbose_name="Comparacion:", null=False, on_delete=models.CASCADE, )
    total_UUID_sat = models.BigIntegerField(verbose_name="UUIDs en archivo SAT:", null=False, unique=False)
    total_UUID_poliza = models.BigIntegerField(verbose_name="UUIDs en archivo Poliza:", null=False, unique=False)
    total_UUID_sat_poliza = models.BigIntegerField(verbose_name="UUIDs del SAT en Poliza:", null=False, unique=False)
    total_UUID_poliza_sat = models.BigIntegerField(verbose_name="UUIDs de Poliza en SAT:", null=False, unique=False)
    total_UUID_sat_no_poliza = models.BigIntegerField(verbose_name="UUIDs del SAT no encontrados en Poliza:", null=False, unique=False)
    total_UUID_poliza_no_sat = models.BigIntegerField(verbose_name="UUIDs de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_folio_sat = models.BigIntegerField(verbose_name="Folios en archivo SAT:", null=False, unique=False)
    total_folio_poliza = models.BigIntegerField(verbose_name="Folios en archivo Poliza:", null=False, unique=False)
    total_folio_sat_no_poliza = models.BigIntegerField(verbose_name="Folios del SAT no encontrados en Poliza:", null=False, unique=False)
    total_folio_poliza_no_sat = models.BigIntegerField(verbose_name="Folios de Poliza no encontrados en SAT:", null=False, unique=False)
    total_folio_sat_poliza = models.BigIntegerField(verbose_name="Folios del SAT  en Poliza:", null=False, unique=False)
    total_folio_poliza_sat = models.BigIntegerField(verbose_name="Folios de la  Poliza en SAT:", null=False, unique=False)
    total_total_sat = models.BigIntegerField(verbose_name="Totales en archivo SAT:", null=False, unique=False)
    total_total_poliza = models.BigIntegerField(verbose_name="Totales en archivo Poliza:", null=False, unique=False)
    total_total_sat_no_poliza = models.BigIntegerField(verbose_name="Totales del SAT no encontrados en Poliza:", null=False, unique=False)
    total_total_poliza_no_sat = models.BigIntegerField(verbose_name="Totales de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_total_sat_poliza = models.BigIntegerField(verbose_name="Totales del SAT en Poliza:", null=False, unique=False)
    total_total_poliza_sat = models.BigIntegerField(verbose_name="Totales de la  Poliza en SAT:", null=False, unique=False)
    total_subtotal_sat = models.BigIntegerField(verbose_name="Sub Totales en archivo SAT:", null=False, unique=False)
    total_subtotal_poliza = models.BigIntegerField(verbose_name="Sub Totales en archivo Poliza:", null=False, unique=False)
    total_subtotal_sat_no_poliza = models.BigIntegerField(verbose_name="Sub Totales del SAT no encontrados en Poliza:", null=False, unique=False)
    total_subtotal_poliza_no_sat = models.BigIntegerField(verbose_name="Sub Totales de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_subtotal_sat_poliza = models.BigIntegerField(verbose_name="Sub Totales del SAT en  Poliza:", null=False, unique=False)
    total_subtotal_poliza_sat = models.BigIntegerField(verbose_name="Sub Totales de la Poliza en SAT:", null=False, unique=False)
    total_iva_sat = models.BigIntegerField(verbose_name="IVA en archivo SAT:", null=False, unique=False)
    total_iva_poliza = models.BigIntegerField(verbose_name="IVA en archivo Poliza:", null=False, unique=False)
    total_iva_sat_no_poliza = models.BigIntegerField(verbose_name="IVA del SAT no encontrados en Poliza:", null=False, unique=False)
    total_iva_poliza_no_sat = models.BigIntegerField(verbose_name="IVA de la Poliza no encontrados en SAT:", null=False, unique=False)
    total_iva_sat_poliza = models.BigIntegerField(verbose_name="IVA del SAT en Poliza:", null=False, unique=False)
    total_iva_poliza_sat = models.BigIntegerField(verbose_name="IVA de la Poliza en SAT:", null=False, unique=False)
    total_rfcemisor_sat = models.BigIntegerField(verbose_name="RFCs Emisor en archivo SAT:", null=False, unique=False)
    total_rfcemisor_poliza = models.BigIntegerField(verbose_name="RFCs Emisor en archivo Poliza:", null=False, unique=False)
    total_rfcemisor_sat_no_poliza = models.BigIntegerField(verbose_name="RFCs Emisor del SAT no encontrados en Poliza:", null=False, unique=False)
    total_rfcemisor_poliza_no_sat = models.BigIntegerField(verbose_name="RFCs Emisor de Poliza no encontrados en SAT:", null=False, unique=False)
    total_rfcemisor_sat_poliza = models.BigIntegerField(verbose_name="RFCs Emisor del SAT en Poliza:",  null=False, unique=False)
    total_rfcemisor_poliza_sat = models.BigIntegerField(verbose_name="RFCs Emisor de la Poliza en SAT:", null=False, unique=False)
    total_rfcreceptor_sat = models.BigIntegerField(verbose_name="RFCs Receptor en archivo SAT:", null=False, unique=False)
    total_rfcreceptor_poliza = models.BigIntegerField(verbose_name="RFCs Receptor en archivo Poliza:", null=False, unique=False)
    total_rfcreceptor_sat_no_poliza = models.BigIntegerField(verbose_name="RFC Receptor de SAT no encontrado en Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_no_sat = models.BigIntegerField(verbose_name="RFC Receptor de Poliza no encontrado en SAT:", null=False, unique=False)
    total_rfcreceptor_sat_poliza = models.BigIntegerField(verbose_name="RFCs Receptor del SAT en archivo Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_sat = models.BigIntegerField(verbose_name="RFCs Receptor de la Poliza en SAT:", null=False, unique=False)
    total_nombreemisor_sat = models.BigIntegerField(verbose_name="Nombre Emisor en archivo SAT:", null=False, unique=False)
    total_nombreemisor_poliza = models.BigIntegerField(verbose_name="Nombre Emisor en archivo Poliza:", null=False, unique=False)
    total_nombreemisor_sat_no_poliza = models.BigIntegerField(verbose_name="Nombre Emisor SAT no encontrado en Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_no_sat = models.BigIntegerField(verbose_name="Nombre Emisor Poliza no encontrado en SAT:", null=False, unique=False)
    total_nombreemisor_sat_poliza = models.BigIntegerField(verbose_name="Nombre Emisor  del SAT en Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_sat = models.BigIntegerField(verbose_name="Nombre Emisor de la Poliza en SAT:", null=False, unique=False)
    total_nombrereceptor_sat = models.BigIntegerField(verbose_name="Nombre Receptor en archivo SAT:", null=False, unique=False)
    total_nombrereceptor_poliza = models.BigIntegerField(verbose_name="Nombre Receptor en archivo Poliza:", null=False, unique=False)
    total_nombrereceptor_sat_no_poliza = models.BigIntegerField(verbose_name="NombreReceptor SAT no coincide en Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_no_sat = models.BigIntegerField(verbose_name="NombreReceptor Poliza no coincide en SAT:", null=False, unique=False)
    total_nombrereceptor_sat_poliza = models.BigIntegerField(verbose_name="Nombre Receptor de SAT en  Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_sat = models.BigIntegerField(verbose_name="Nombre Receptor de la  Poliza  en SAT:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de comparación:", auto_now=True, null=False, blank=False)
    registro_comparacion = models.CharField(verbose_name="Registro de Comparación:", null=False, blank=False, max_length=200,)

    class Meta:
        verbose_name = "Cifras de Comparación por Fecha"
        verbose_name_plural = "Cifras de Comparación por Fecha"

    def __str__(self):  # __unicode__ on Python 2
        return self.fechas_comparacion.id_key + '-' + self.registro_comparacion


class Diferencias(models.Model):
    #modelo para guardar las diferencias encontradas al comparar
    field_sat = models.ForeignKey(DatosArchivo, verbose_name="Registro SAT:", on_delete=models.CASCADE, null=True)
    field_poliza = models.ForeignKey(DatosPoliza, verbose_name="Registro Poliza:", on_delete=models.CASCADE, null=True)
    field_sat_value = models.CharField(verbose_name="Valor en SAT:", max_length=200, null=False, blank=True, unique=False)
    field_poliza_value = models.CharField(verbose_name="Valor en Poliza:", max_length=200, null=False, blank=True, unique=False)
    diferencia = models.CharField(verbose_name="Atributo:", max_length=200, null=False, blank=True, unique=False)
    nivel_comparacion = models.CharField(verbose_name="Nivel de Comparación:", max_length=200, null=False, blank=True, unique=False)
    source = models.CharField(verbose_name="Archivo Fuente:", max_length=200, null=False, blank=True, unique=False)
    comparacion = models.ForeignKey(CompararArchivos, verbose_name="Comparación:", null=False, on_delete=models.CASCADE,)


    class Meta:
        verbose_name = "Diferencia de Archivos"
        verbose_name_plural = "Diferencias de Archivos"

    def __str__(self):  # __unicode__ on Python 2
        return self.comparacion.id_key + '-' + self.diferencia


class DiferenciasFecha(models.Model):
    #modelo para guardar las diferencias encontradas al comparar
    field_sat = models.ForeignKey(DatosArchivo, verbose_name="Registro SAT:", on_delete=models.CASCADE, null=True)
    field_poliza = models.ForeignKey(DatosPoliza, verbose_name="Registro Poliza:", on_delete=models.CASCADE, null=True)
    field_sat_value = models.CharField(verbose_name="Valor en SAT:", max_length=200, null=False, blank=True, unique=False)
    field_poliza_value = models.CharField(verbose_name="Valor en Poliza:", max_length=200, null=False, blank=True, unique=False)
    diferencia = models.CharField(verbose_name="Atributo:", max_length=200, null=False, blank=True, unique=False)
    nivel_comparacion = models.CharField(verbose_name="Nivel de Comparación:", max_length=200, null=False, blank=True, unique=False)
    source = models.CharField(verbose_name="Archivo Fuente:", max_length=200, null=False, blank=True, unique=False)
    comparacion = models.ForeignKey(CompararPorFecha, verbose_name="Comparación:", null=False, on_delete=models.CASCADE,)


    class Meta:
        verbose_name = "Diferencia de Archivos por Fecha"
        verbose_name_plural = "Diferencias de Archivos por Fecha"

    def __str__(self):  # __unicode__ on Python 2
        return self.comparacion.id_key + '-' + self.diferencia


class LogEventos(models.Model):
    #log para registrar acciones realizadas en el sistema -- bitacora
    accion = models.CharField(verbose_name="Acción", max_length=200, null=False, blank=True, unique=False)
    registros_procesados = models.BigIntegerField(verbose_name="Total de registros procesados", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de proceso", auto_now=True, null=False, blank=False)
    usuario_proceso = models.ForeignKey(User, verbose_name="Usuario", blank="False", null=False, related_name="Usuario", on_delete=models.CASCADE,)

    class Meta:
        verbose_name = "Log de Eventos"
        verbose_name_plural = "Log de Eventos"

    def __str__(self):  # __unicode__ on Python 2
        return self.accion
