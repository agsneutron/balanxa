
from django.db import models
from django.core.validators import FileExtensionValidator


class Procesa(models.Model):
    archivo = models.FileField(verbose_name="Archivo SAT",  null=False, blank=False)
    fecha = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Archivo SAT"
        verbose_name_plural = "Archivos SAT"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo.name + ' - ' + self.fecha


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
        return self.archivo.name + ' - ' + self.fecha


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


class Comparar_UUID(models.Model):
    archivo_sat = models.ForeignKey(Procesa, verbose_name="Archivo SAT:", null=False, on_delete=False,)
    archivo_poliza = models.ForeignKey(PolizaArchivo, verbose_name="Archivo Poliza:", null=False, on_delete=False, )
    total_UUID_sat = models.BigIntegerField(verbose_name="Total de UUID SAT:", null=False, unique=False)
    total_UUID_poliza = models.BigIntegerField(verbose_name="Total de UUID Poliza:", null=False, unique=False)
    total_sat_no_poliza = models.BigIntegerField(verbose_name="Total de UUID SAT no Poliza:", null=False, unique=False)
    total_poliza_no_sat = models.BigIntegerField(verbose_name="Total de UUID Poliza no SAT:", null=False, unique=False)
    fecha_proceso = models.DateTimeField(verbose_name="Fecha / Hora de carga:", auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Comparación UUID"
        verbose_name_plural = "Comparaciones UUID"

    def __str__(self):  # __unicode__ on Python 2
        return self.archivo_sat.name + '-' + self.archivo_poliza.name + '-' + self.fecha_proceso


class DiferenciasUUID(models.Model):
    UUID_sat = models.CharField(verbose_name="UUID SAT", max_length=200, null=False,
                                         blank=True, unique=False)
    UUID_poliza = models.CharField(verbose_name="UUID Poliza", max_length=200, null=False,
                                         blank=True, unique=False)
    comparacion = models.ForeignKey(Comparar_UUID, verbose_name="Comparación", null=False, on_delete=False,)
