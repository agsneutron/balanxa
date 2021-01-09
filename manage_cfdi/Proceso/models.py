
from django.db import models
from django.core.validators import FileExtensionValidator


class Procesa(models.Model):
    archivo = models.FileField(verbose_name="Archivo SAT",  null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Archivo SAT"
        verbose_name_plural = "Archivos SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class DatosArchivo(models.Model):
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
    fechaemision = models.CharField(verbose_name="Fecha de Timbrado", max_length=200, null=False, blank=True, unique=False)
    estatus = models.CharField(verbose_name="Estatus", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Datos del PKT SAT"
        verbose_name_plural = "Datos del PKT SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.uuid


class DatosLog(models.Model):
    identificador_archivo = models.CharField(verbose_name="Identificador del archivo", max_length=200, null=False,
                                             blank=True, unique=False)
    identificador_pkt = models.CharField(verbose_name="Identificador del paquete", max_length=200, null=False,
                                         blank=True, unique=False)
    atributo = models.CharField(verbose_name="Atributo", max_length=200, null=False,
                                         blank=True, unique=False)


    class Meta:
        verbose_name = "Log datos SAT"
        verbose_name_plural = "Log datos SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.atributo


class PolizaArchivo(models.Model):
    archivo = models.FileField(verbose_name="Archivo",  null=False, blank=False, validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])])
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Archivo Poliza"
        verbose_name_plural = "Archivos Polizas"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class DatosPoliza(models.Model):
    identificador_archivo = models.ForeignKey(PolizaArchivo, verbose_name="Identificador del Archivo", on_delete=models.CASCADE, )
    NO_FACTURA = models.CharField(verbose_name="No. Factura", max_length=200, null=False, blank=True, unique=False)
    SERIE = models.CharField(verbose_name="Serie", max_length=200, null=False, blank=True, unique=False)
    NOMBRE_RECEPTOR = models.CharField(verbose_name="Nombre Rceptor", max_length=200, null=False, blank=True, unique=False)
    RFC_RECEPTOR = models.CharField(verbose_name="RFC Receptor", max_length=200, null=False, blank=True, unique=False)
    NOMBRE_EMISOR = models.CharField(verbose_name="Nombre Emisor", max_length=200, null=False, blank=True, unique=False)
    RFC_EMISOR = models.CharField(verbose_name="RFC Emisor", max_length=200, null=False, blank=True, unique=False)
    FORMA_PAGO = models.CharField(verbose_name="Forma de Pago", max_length=200, null=False, blank=True, unique=False)
    FECHA_EMISION = models.CharField(verbose_name="Fecha de Emmisión", max_length=200, null=False, blank=True, unique=False)
    TIPO_FACTURA = models.CharField(verbose_name="Tipo de Factura", max_length=200, null=False, blank=True, unique=False)
    TIPO_MONEDA = models.CharField(verbose_name="Tipo de Moneda", max_length=200, null=False, blank=True, unique=False)
    SUBTOTAL = models.CharField(verbose_name="Sub Total", max_length=200, null=False, blank=True, unique=False)
    IVA = models.CharField(verbose_name="IVA", max_length=200, null=False, blank=True, unique=False)
    DESCUENTO = models.CharField(verbose_name="Descuento", max_length=200, null=False, blank=True, unique=False)
    TOTAL = models.CharField(verbose_name="Total", max_length=200, null=False, blank=True, unique=False)
    SALDO = models.CharField(verbose_name="Saldo", max_length=200, null=False, blank=True, unique=False)
    FECHA_CREO_XML = models.CharField(verbose_name="Fecha de Creación de XML", max_length=200, null=False, blank=True, unique=False)
    TIMBRE_UUID = models.CharField(verbose_name="Timbre UUID", max_length=200, null=False, blank=True, unique=False)
    METODO_PAGO = models.CharField(verbose_name="Método de Pago", max_length=200, null=False, blank=True, unique=False)
    ESTATUS = models.CharField(verbose_name="Estatus", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Datos de la Poliza"
        verbose_name_plural = "Datos de las Polizas"

    def __str__(self):  # __unicode__ on Python 2
        return self.NO_FACTURA


class DatosPolizaLog(models.Model):
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
    archivo = models.ForeignKey(PolizaArchivo, verbose_name="Archivo:", null=False, on_delete=models.CASCADE,)
    total_procesado = models.BigIntegerField(verbose_name="Total de Registros procesados:", null=False, unique=False)
    total_error = models.BigIntegerField(verbose_name="Total de registros con error:", null=False, unique=False)
    total_exito = models.BigIntegerField(verbose_name="Total de registros correctos:", null=False, unique=False)
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Log de Registros Procesados"
        verbose_name_plural = "Log de Registros PRocesados"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name


class CompararArchivos(models.Model):
    archivo_sat = models.ForeignKey(Procesa, verbose_name="Archivo SAT:", null=False, on_delete=False,)
    archivo_poliza = models.ForeignKey(PolizaArchivo, verbose_name="Archivo Poliza:", null=False, on_delete=False, )
    total_registros_sat = models.BigIntegerField(verbose_name="Total de registros SAT:", null=False, unique=False)
    total_registros_poliza = models.BigIntegerField(verbose_name="Total de registros Poliza:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)
    id_key = models.CharField(verbose_name="Comparación", max_length=200, null=False, blank=True, unique=False)

    class Meta:
        verbose_name = "Comparación Archivos"
        verbose_name_plural = "Comparaciones Archivos"

    def __str__(self):  # __unicode__ on Python 2
        return self.id_key + '-' + self.archivo_sat.archivo.name + '-' + self.archivo_poliza.archivo.name


class CifrasComparacion(models.Model):
    archivos_comparados = models.ForeignKey(CompararArchivos, verbose_name="Comparacion:", null=False, on_delete=False, )
    total_UUID_sat = models.BigIntegerField(verbose_name="Total de UUID SAT:", null=False, unique=False)
    total_UUID_poliza = models.BigIntegerField(verbose_name="Total de UUID Poliza:", null=False, unique=False)
    total_UUID_sat_poliza = models.BigIntegerField(verbose_name="Total de UUID SAT Poliza:", null=False, unique=False)
    total_UUID_poliza_sat = models.BigIntegerField(verbose_name="Total de UUID Poliza SAT:", null=False, unique=False)
    total_UUID_sat_no_poliza = models.BigIntegerField(verbose_name="Total de UUID SAT no Poliza:", null=False, unique=False)
    total_UUID_poliza_no_sat = models.BigIntegerField(verbose_name="Total de UUID Poliza no SAT:", null=False, unique=False)
    total_folio_sat = models.BigIntegerField(verbose_name="Total de Folio SAT:", null=False, unique=False)
    total_folio_poliza = models.BigIntegerField(verbose_name="Total de Folio Poliza:", null=False, unique=False)
    total_folio_sat_no_poliza = models.BigIntegerField(verbose_name="Total de Folio SAT no Poliza:", null=False, unique=False)
    total_folio_poliza_no_sat = models.BigIntegerField(verbose_name="Total de Folio Poliza no SAT:", null=False, unique=False)
    total_folio_sat_poliza = models.BigIntegerField(verbose_name="Total de Folio SAT Poliza:", null=False, unique=False)
    total_folio_poliza_sat = models.BigIntegerField(verbose_name="Total de Folio Poliza SAT:", null=False, unique=False)
    total_total_sat = models.BigIntegerField(verbose_name="Total de Total SAT:", null=False, unique=False)
    total_total_poliza = models.BigIntegerField(verbose_name="Total de Total Poliza:", null=False, unique=False)
    total_total_sat_no_poliza = models.BigIntegerField(verbose_name="Total de Total SAT no Poliza:", null=False, unique=False)
    total_total_poliza_no_sat = models.BigIntegerField(verbose_name="Total de Total Poliza no SAT:", null=False, unique=False)
    total_total_sat_poliza = models.BigIntegerField(verbose_name="Total de Total SAT Poliza:", null=False, unique=False)
    total_total_poliza_sat = models.BigIntegerField(verbose_name="Total de Total Poliza SAT:", null=False, unique=False)
    total_subtotal_sat = models.BigIntegerField(verbose_name="Total de Sub Total SAT:", null=False, unique=False)
    total_subtotal_poliza = models.BigIntegerField(verbose_name="Total de Sub Total Poliza:", null=False, unique=False)
    total_subtotal_sat_no_poliza = models.BigIntegerField(verbose_name="Total de Sub Total SAT no Poliza:", null=False, unique=False)
    total_subtotal_poliza_no_sat = models.BigIntegerField(verbose_name="Total de Sub Total Poliza no SAT:", null=False, unique=False)
    total_subtotal_sat_poliza = models.BigIntegerField(verbose_name="Total de Sub Total SAT Poliza:", null=False, unique=False)
    total_subtotal_poliza_sat = models.BigIntegerField(verbose_name="Total de Sub Total Poliza SAT:", null=False, unique=False)
    total_iva_sat = models.BigIntegerField(verbose_name="Total de IVA SAT:", null=False, unique=False)
    total_iva_poliza = models.BigIntegerField(verbose_name="Total de IVA Poliza:", null=False, unique=False)
    total_iva_sat_no_poliza = models.BigIntegerField(verbose_name="Total de IVA SAT no Poliza:", null=False, unique=False)
    total_iva_poliza_no_sat = models.BigIntegerField(verbose_name="Total de IVA Poliza no SAT:", null=False, unique=False)
    total_iva_sat_poliza = models.BigIntegerField(verbose_name="Total de IVA SAT Poliza:", null=False, unique=False)
    total_iva_poliza_sat = models.BigIntegerField(verbose_name="Total de IVA Poliza SAT:", null=False, unique=False)
    total_rfcemisor_sat = models.BigIntegerField(verbose_name="Total de RFC Emisor SAT:", null=False, unique=False)
    total_rfcemisor_poliza = models.BigIntegerField(verbose_name="Total de RFC Emisor Poliza:", null=False, unique=False)
    total_rfcemisor_sat_no_poliza = models.BigIntegerField(verbose_name="Total de RFC Emisor SAT no Poliza:", null=False, unique=False)
    total_rfcemisor_poliza_no_sat = models.BigIntegerField(verbose_name="Total de RFC Emisor Poliza no SAT:", null=False, unique=False)
    total_rfcemisor_sat_poliza = models.BigIntegerField(verbose_name="Total de RFC Emisor SAT Poliza:",  null=False, unique=False)
    total_rfcemisor_poliza_sat = models.BigIntegerField(verbose_name="Total de RFC Emisor Poliza SAT:", null=False, unique=False)
    total_rfcreceptor_sat = models.BigIntegerField(verbose_name="Total de RFC Receptor SAT:", null=False, unique=False)
    total_rfcreceptor_poliza = models.BigIntegerField(verbose_name="Total de RFC Receptor Poliza:", null=False, unique=False)
    total_rfcreceptor_sat_no_poliza = models.BigIntegerField(verbose_name="Total de RFC Receptor SAT no Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_no_sat = models.BigIntegerField(verbose_name="Total de RFC Receptor Poliza no SAT:", null=False, unique=False)
    total_rfcreceptor_sat_poliza = models.BigIntegerField(verbose_name="Total de RFC Receptor SAT Poliza:", null=False, unique=False)
    total_rfcreceptor_poliza_sat = models.BigIntegerField(verbose_name="Total de RFC Receptor Poliza SAT:", null=False, unique=False)
    total_nombreemisor_sat = models.BigIntegerField(verbose_name="Total de Nombre Emisor SAT:", null=False, unique=False)
    total_nombreemisor_poliza = models.BigIntegerField(verbose_name="Total de Nombre Emisor Poliza:", null=False, unique=False)
    total_nombreemisor_sat_no_poliza = models.BigIntegerField(verbose_name="Total de Nombre Emisor SAT no Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_no_sat = models.BigIntegerField(verbose_name="Total de Nombre Emisor Poliza no SAT:", null=False, unique=False)
    total_nombreemisor_sat_poliza = models.BigIntegerField(verbose_name="Total de Nombre Emisor SAT Poliza:", null=False, unique=False)
    total_nombreemisor_poliza_sat = models.BigIntegerField(verbose_name="Total de Nombre Emisor Poliza SAT:", null=False, unique=False)
    total_nombrereceptor_sat = models.BigIntegerField(verbose_name="Total de Nombre Receptor SAT:", null=False, unique=False)
    total_nombrereceptor_poliza = models.BigIntegerField(verbose_name="Total de Nombre Receptor Poliza:", null=False, unique=False)
    total_nombrereceptor_sat_no_poliza = models.BigIntegerField(verbose_name="Total de Nombre Receptor SAT no Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_no_sat = models.BigIntegerField(verbose_name="Total de Nombre Receptor Poliza no SAT:", null=False, unique=False)
    total_nombrereceptor_sat_poliza = models.BigIntegerField(verbose_name="Total de Nombre Receptor SAT Poliza:", null=False, unique=False)
    total_nombrereceptor_poliza_sat = models.BigIntegerField(verbose_name="Total de Nombre Receptor Poliza SAT:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de comparación:", auto_now=True, null=False, blank=False)


class Diferencias(models.Model):
    #field_sat = models.CharField(verbose_name="Registro SAT:", max_length=200, null=False, blank=True, unique=False)
    #field_poliza = models.CharField(verbose_name="Registro Poliza:", max_length=200, null=False, blank=True, unique=False)
    field_sat = models.ForeignKey(DatosArchivo,verbose_name="Registro SAT:", on_delete=False, null=True)
    field_poliza = models.ForeignKey(DatosPoliza,verbose_name="Registro Poliza:", on_delete=False, null=True)
    diferencia = models.CharField(verbose_name="Diferencia:", max_length=200, null=False, blank=True, unique=False)
    nivel_comparacion = models.CharField(verbose_name="Nivel de Comparación:", max_length=200, null=False, blank=True, unique=False)
    source = models.CharField(verbose_name="Archivo Fuente:", max_length=200, null=False, blank=True, unique=False)
    comparacion = models.ForeignKey(CompararArchivos, verbose_name="Comparación:", null=False, on_delete=False,)
