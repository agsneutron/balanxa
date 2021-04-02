# Generated by Django 3.1.4 on 2021-01-28 03:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Proceso', '0005_auto_20210109_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='CifrasComparacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_UUID_sat', models.BigIntegerField(verbose_name='UUIDs en archivo SAT:')),
                ('total_UUID_poliza', models.BigIntegerField(verbose_name='UUIDs en archivo Poliza:')),
                ('total_UUID_sat_poliza', models.BigIntegerField(verbose_name='UUIDs del SAT en Poliza:')),
                ('total_UUID_poliza_sat', models.BigIntegerField(verbose_name='UUIDs de Poliza en SAT:')),
                ('total_UUID_sat_no_poliza', models.BigIntegerField(verbose_name='UUIDs del SAT no encontrados en Poliza:')),
                ('total_UUID_poliza_no_sat', models.BigIntegerField(verbose_name='UUIDs de la Poliza no encontrados en SAT:')),
                ('total_folio_sat', models.BigIntegerField(verbose_name='Folios en archivo SAT:')),
                ('total_folio_poliza', models.BigIntegerField(verbose_name='Folios en archivo Poliza:')),
                ('total_folio_sat_no_poliza', models.BigIntegerField(verbose_name='Folios del SAT no encontrados en Poliza:')),
                ('total_folio_poliza_no_sat', models.BigIntegerField(verbose_name='Folios de Poliza no encontrados en SAT:')),
                ('total_folio_sat_poliza', models.BigIntegerField(verbose_name='Folios del SAT  en Poliza:')),
                ('total_folio_poliza_sat', models.BigIntegerField(verbose_name='Folios de la  Poliza en SAT:')),
                ('total_total_sat', models.BigIntegerField(verbose_name='Totales en archivo SAT:')),
                ('total_total_poliza', models.BigIntegerField(verbose_name='Totales en archivo Poliza:')),
                ('total_total_sat_no_poliza', models.BigIntegerField(verbose_name='Totales del SAT no encontrados en Poliza:')),
                ('total_total_poliza_no_sat', models.BigIntegerField(verbose_name='Totales de la Poliza no encontrados en SAT:')),
                ('total_total_sat_poliza', models.BigIntegerField(verbose_name='Totales del SAT en Poliza:')),
                ('total_total_poliza_sat', models.BigIntegerField(verbose_name='Totales de la  Poliza en SAT:')),
                ('total_subtotal_sat', models.BigIntegerField(verbose_name='Sub Totales en archivo SAT:')),
                ('total_subtotal_poliza', models.BigIntegerField(verbose_name='Sub Totales en archivo Poliza:')),
                ('total_subtotal_sat_no_poliza', models.BigIntegerField(verbose_name='Sub Totales del SAT no encontrados en Poliza:')),
                ('total_subtotal_poliza_no_sat', models.BigIntegerField(verbose_name='Sub Totales de la Poliza no encontrados en SAT:')),
                ('total_subtotal_sat_poliza', models.BigIntegerField(verbose_name='Sub Totales del SAT en  Poliza:')),
                ('total_subtotal_poliza_sat', models.BigIntegerField(verbose_name='Sub Totales de la Poliza en SAT:')),
                ('total_iva_sat', models.BigIntegerField(verbose_name='IVA en archivo SAT:')),
                ('total_iva_poliza', models.BigIntegerField(verbose_name='IVA en archivo Poliza:')),
                ('total_iva_sat_no_poliza', models.BigIntegerField(verbose_name='IVA del SAT no encontrados en Poliza:')),
                ('total_iva_poliza_no_sat', models.BigIntegerField(verbose_name='IVA de la Poliza no encontrados en SAT:')),
                ('total_iva_sat_poliza', models.BigIntegerField(verbose_name='IVA del SAT en Poliza:')),
                ('total_iva_poliza_sat', models.BigIntegerField(verbose_name='IVA de la Poliza en SAT:')),
                ('total_rfcemisor_sat', models.BigIntegerField(verbose_name='RFCs Emisor en archivo SAT:')),
                ('total_rfcemisor_poliza', models.BigIntegerField(verbose_name='RFCs Emisor en archivo Poliza:')),
                ('total_rfcemisor_sat_no_poliza', models.BigIntegerField(verbose_name='RFCs Emisor del SAT no encontrados en Poliza:')),
                ('total_rfcemisor_poliza_no_sat', models.BigIntegerField(verbose_name='RFCs Emisor de Poliza no encontrados en SAT:')),
                ('total_rfcemisor_sat_poliza', models.BigIntegerField(verbose_name='RFCs Emisor del SAT en Poliza:')),
                ('total_rfcemisor_poliza_sat', models.BigIntegerField(verbose_name='RFCs Emisor de la Poliza en SAT:')),
                ('total_rfcreceptor_sat', models.BigIntegerField(verbose_name='RFCs Receptor en archivo SAT:')),
                ('total_rfcreceptor_poliza', models.BigIntegerField(verbose_name='RFCs Receptor en archivo Poliza:')),
                ('total_rfcreceptor_sat_no_poliza', models.BigIntegerField(verbose_name='RFC Receptor de SAT no encontrado en Poliza:')),
                ('total_rfcreceptor_poliza_no_sat', models.BigIntegerField(verbose_name='RFC Receptor de Poliza no encontrado en SAT:')),
                ('total_rfcreceptor_sat_poliza', models.BigIntegerField(verbose_name='RFCs Receptor del SAT en archivo Poliza:')),
                ('total_rfcreceptor_poliza_sat', models.BigIntegerField(verbose_name='RFCs Receptor de la Poliza en SAT:')),
                ('total_nombreemisor_sat', models.BigIntegerField(verbose_name='Nombre Emisor en archivo SAT:')),
                ('total_nombreemisor_poliza', models.BigIntegerField(verbose_name='Nombre Emisor en archivo Poliza:')),
                ('total_nombreemisor_sat_no_poliza', models.BigIntegerField(verbose_name='Nombre Emisor SAT no encontrado en Poliza:')),
                ('total_nombreemisor_poliza_no_sat', models.BigIntegerField(verbose_name='Nombre Emisor Poliza no encontrado en SAT:')),
                ('total_nombreemisor_sat_poliza', models.BigIntegerField(verbose_name='Nombre Emisor  del SAT en Poliza:')),
                ('total_nombreemisor_poliza_sat', models.BigIntegerField(verbose_name='Nombre Emisor de la Poliza en SAT:')),
                ('total_nombrereceptor_sat', models.BigIntegerField(verbose_name='Nombre Receptor en archivo SAT:')),
                ('total_nombrereceptor_poliza', models.BigIntegerField(verbose_name='Nombre Receptor en archivo Poliza:')),
                ('total_nombrereceptor_sat_no_poliza', models.BigIntegerField(verbose_name='NombreReceptor SAT no coincide en Poliza:')),
                ('total_nombrereceptor_poliza_no_sat', models.BigIntegerField(verbose_name='NombreReceptor Poliza no coincide en SAT:')),
                ('total_nombrereceptor_sat_poliza', models.BigIntegerField(verbose_name='Nombre Receptor de SAT en  Poliza:')),
                ('total_nombrereceptor_poliza_sat', models.BigIntegerField(verbose_name='Nombre Receptor de la  Poliza  en SAT:')),
                ('fecha_proceso', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de comparación:')),
                ('registro_comparacion', models.CharField(max_length=200, verbose_name='Registro de Comparación:')),
            ],
            options={
                'verbose_name': 'Cifras de Comparación de Archivos',
                'verbose_name_plural': 'Cifras de Comparación de Archivos',
            },
        ),
        migrations.CreateModel(
            name='CifrasComparacionFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_UUID_sat', models.BigIntegerField(verbose_name='UUIDs en archivo SAT:')),
                ('total_UUID_poliza', models.BigIntegerField(verbose_name='UUIDs en archivo Poliza:')),
                ('total_UUID_sat_poliza', models.BigIntegerField(verbose_name='UUIDs del SAT en Poliza:')),
                ('total_UUID_poliza_sat', models.BigIntegerField(verbose_name='UUIDs de Poliza en SAT:')),
                ('total_UUID_sat_no_poliza', models.BigIntegerField(verbose_name='UUIDs del SAT no encontrados en Poliza:')),
                ('total_UUID_poliza_no_sat', models.BigIntegerField(verbose_name='UUIDs de la Poliza no encontrados en SAT:')),
                ('total_folio_sat', models.BigIntegerField(verbose_name='Folios en archivo SAT:')),
                ('total_folio_poliza', models.BigIntegerField(verbose_name='Folios en archivo Poliza:')),
                ('total_folio_sat_no_poliza', models.BigIntegerField(verbose_name='Folios del SAT no encontrados en Poliza:')),
                ('total_folio_poliza_no_sat', models.BigIntegerField(verbose_name='Folios de Poliza no encontrados en SAT:')),
                ('total_folio_sat_poliza', models.BigIntegerField(verbose_name='Folios del SAT  en Poliza:')),
                ('total_folio_poliza_sat', models.BigIntegerField(verbose_name='Folios de la  Poliza en SAT:')),
                ('total_total_sat', models.BigIntegerField(verbose_name='Totales en archivo SAT:')),
                ('total_total_poliza', models.BigIntegerField(verbose_name='Totales en archivo Poliza:')),
                ('total_total_sat_no_poliza', models.BigIntegerField(verbose_name='Totales del SAT no encontrados en Poliza:')),
                ('total_total_poliza_no_sat', models.BigIntegerField(verbose_name='Totales de la Poliza no encontrados en SAT:')),
                ('total_total_sat_poliza', models.BigIntegerField(verbose_name='Totales del SAT en Poliza:')),
                ('total_total_poliza_sat', models.BigIntegerField(verbose_name='Totales de la  Poliza en SAT:')),
                ('total_subtotal_sat', models.BigIntegerField(verbose_name='Sub Totales en archivo SAT:')),
                ('total_subtotal_poliza', models.BigIntegerField(verbose_name='Sub Totales en archivo Poliza:')),
                ('total_subtotal_sat_no_poliza', models.BigIntegerField(verbose_name='Sub Totales del SAT no encontrados en Poliza:')),
                ('total_subtotal_poliza_no_sat', models.BigIntegerField(verbose_name='Sub Totales de la Poliza no encontrados en SAT:')),
                ('total_subtotal_sat_poliza', models.BigIntegerField(verbose_name='Sub Totales del SAT en  Poliza:')),
                ('total_subtotal_poliza_sat', models.BigIntegerField(verbose_name='Sub Totales de la Poliza en SAT:')),
                ('total_iva_sat', models.BigIntegerField(verbose_name='IVA en archivo SAT:')),
                ('total_iva_poliza', models.BigIntegerField(verbose_name='IVA en archivo Poliza:')),
                ('total_iva_sat_no_poliza', models.BigIntegerField(verbose_name='IVA del SAT no encontrados en Poliza:')),
                ('total_iva_poliza_no_sat', models.BigIntegerField(verbose_name='IVA de la Poliza no encontrados en SAT:')),
                ('total_iva_sat_poliza', models.BigIntegerField(verbose_name='IVA del SAT en Poliza:')),
                ('total_iva_poliza_sat', models.BigIntegerField(verbose_name='IVA de la Poliza en SAT:')),
                ('total_rfcemisor_sat', models.BigIntegerField(verbose_name='RFCs Emisor en archivo SAT:')),
                ('total_rfcemisor_poliza', models.BigIntegerField(verbose_name='RFCs Emisor en archivo Poliza:')),
                ('total_rfcemisor_sat_no_poliza', models.BigIntegerField(verbose_name='RFCs Emisor del SAT no encontrados en Poliza:')),
                ('total_rfcemisor_poliza_no_sat', models.BigIntegerField(verbose_name='RFCs Emisor de Poliza no encontrados en SAT:')),
                ('total_rfcemisor_sat_poliza', models.BigIntegerField(verbose_name='RFCs Emisor del SAT en Poliza:')),
                ('total_rfcemisor_poliza_sat', models.BigIntegerField(verbose_name='RFCs Emisor de la Poliza en SAT:')),
                ('total_rfcreceptor_sat', models.BigIntegerField(verbose_name='RFCs Receptor en archivo SAT:')),
                ('total_rfcreceptor_poliza', models.BigIntegerField(verbose_name='RFCs Receptor en archivo Poliza:')),
                ('total_rfcreceptor_sat_no_poliza', models.BigIntegerField(verbose_name='RFC Receptor de SAT no encontrado en Poliza:')),
                ('total_rfcreceptor_poliza_no_sat', models.BigIntegerField(verbose_name='RFC Receptor de Poliza no encontrado en SAT:')),
                ('total_rfcreceptor_sat_poliza', models.BigIntegerField(verbose_name='RFCs Receptor del SAT en archivo Poliza:')),
                ('total_rfcreceptor_poliza_sat', models.BigIntegerField(verbose_name='RFCs Receptor de la Poliza en SAT:')),
                ('total_nombreemisor_sat', models.BigIntegerField(verbose_name='Nombre Emisor en archivo SAT:')),
                ('total_nombreemisor_poliza', models.BigIntegerField(verbose_name='Nombre Emisor en archivo Poliza:')),
                ('total_nombreemisor_sat_no_poliza', models.BigIntegerField(verbose_name='Nombre Emisor SAT no encontrado en Poliza:')),
                ('total_nombreemisor_poliza_no_sat', models.BigIntegerField(verbose_name='Nombre Emisor Poliza no encontrado en SAT:')),
                ('total_nombreemisor_sat_poliza', models.BigIntegerField(verbose_name='Nombre Emisor  del SAT en Poliza:')),
                ('total_nombreemisor_poliza_sat', models.BigIntegerField(verbose_name='Nombre Emisor de la Poliza en SAT:')),
                ('total_nombrereceptor_sat', models.BigIntegerField(verbose_name='Nombre Receptor en archivo SAT:')),
                ('total_nombrereceptor_poliza', models.BigIntegerField(verbose_name='Nombre Receptor en archivo Poliza:')),
                ('total_nombrereceptor_sat_no_poliza', models.BigIntegerField(verbose_name='NombreReceptor SAT no coincide en Poliza:')),
                ('total_nombrereceptor_poliza_no_sat', models.BigIntegerField(verbose_name='NombreReceptor Poliza no coincide en SAT:')),
                ('total_nombrereceptor_sat_poliza', models.BigIntegerField(verbose_name='Nombre Receptor de SAT en  Poliza:')),
                ('total_nombrereceptor_poliza_sat', models.BigIntegerField(verbose_name='Nombre Receptor de la  Poliza  en SAT:')),
                ('fecha_proceso', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de comparación:')),
                ('registro_comparacion', models.CharField(max_length=200, verbose_name='Registro de Comparación:')),
            ],
            options={
                'verbose_name': 'Cifras de Comparación por Fecha',
                'verbose_name_plural': 'Cifras de Comparación por Fecha',
            },
        ),
        migrations.CreateModel(
            name='CompararArchivos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_registros_sat', models.BigIntegerField(verbose_name='Total de registros SAT:')),
                ('total_registros_poliza', models.BigIntegerField(verbose_name='Total de registros Poliza:')),
                ('fecha_proceso', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga:')),
                ('id_key', models.CharField(blank=True, max_length=200, verbose_name='Comparación')),
            ],
            options={
                'verbose_name': 'Comparación Archivos',
                'verbose_name_plural': 'Comparaciones Archivos',
            },
        ),
        migrations.CreateModel(
            name='CompararPorFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(verbose_name='Fecha inicio')),
                ('fecha_fin', models.DateTimeField(verbose_name='Fecha fin')),
                ('total_registros_sat', models.BigIntegerField(verbose_name='Total de registros SAT')),
                ('total_registros_poliza', models.BigIntegerField(verbose_name='Total de registros Poliza')),
                ('fecha_proceso', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga')),
                ('id_key', models.CharField(blank=True, max_length=200, verbose_name='Comparación')),
            ],
            options={
                'verbose_name': 'Comparación de Archivos por Fecha',
                'verbose_name_plural': 'Comparaciones de Archivos por Fecha',
            },
        ),
        migrations.CreateModel(
            name='ConteoXMLLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_error', models.BigIntegerField(verbose_name='Total de atributos con error:')),
                ('total_exito', models.BigIntegerField(verbose_name='Total de atributos correctos:')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga:')),
            ],
            options={
                'verbose_name': 'Cifras de Registros Procesados XML',
                'verbose_name_plural': 'Cifras de Registros Procesados XML',
            },
        ),
        migrations.CreateModel(
            name='Diferencias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_sat_value', models.CharField(blank=True, max_length=200, verbose_name='Valor en SAT:')),
                ('field_poliza_value', models.CharField(blank=True, max_length=200, verbose_name='Valor en Poliza:')),
                ('diferencia', models.CharField(blank=True, max_length=200, verbose_name='Atributo:')),
                ('nivel_comparacion', models.CharField(blank=True, max_length=200, verbose_name='Nivel de Comparación:')),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='Archivo Fuente:')),
                ('comparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.comparararchivos', verbose_name='Comparación:')),
            ],
            options={
                'verbose_name': 'Diferencia de Archivos',
                'verbose_name_plural': 'Diferencias de Archivos',
            },
        ),
        migrations.CreateModel(
            name='DiferenciasFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_sat_value', models.CharField(blank=True, max_length=200, verbose_name='Valor en SAT:')),
                ('field_poliza_value', models.CharField(blank=True, max_length=200, verbose_name='Valor en Poliza:')),
                ('diferencia', models.CharField(blank=True, max_length=200, verbose_name='Atributo:')),
                ('nivel_comparacion', models.CharField(blank=True, max_length=200, verbose_name='Nivel de Comparación:')),
                ('source', models.CharField(blank=True, max_length=200, verbose_name='Archivo Fuente:')),
                ('comparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.compararporfecha', verbose_name='Comparación:')),
            ],
            options={
                'verbose_name': 'Diferencia de Archivos por Fecha',
                'verbose_name_plural': 'Diferencias de Archivos por Fecha',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=200, unique=True, verbose_name='Nombre de la Empresa')),
                ('membresia', models.BigIntegerField(blank=True, verbose_name='Membresia')),
                ('rfc', models.CharField(blank=True, max_length=200, unique=True, verbose_name='RFC de la Empresa')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='LogEventos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(blank=True, max_length=200, verbose_name='Acción')),
                ('registros_procesados', models.BigIntegerField(verbose_name='Total de registros procesados')),
                ('fecha_proceso', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de proceso')),
                ('usuario_proceso', models.ForeignKey(blank='False', on_delete=django.db.models.deletion.CASCADE, related_name='Usuario', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Log de Eventos',
                'verbose_name_plural': 'Log de Eventos',
            },
        ),
        migrations.RemoveField(
            model_name='diferenciasuuid',
            name='comparacion',
        ),
        migrations.AlterModelOptions(
            name='conteopolizalog',
            options={'verbose_name': 'Cifras de Registros Procesados POLIZA', 'verbose_name_plural': 'Cifras de Registros Procesados POLIZA'},
        ),
        migrations.AlterModelOptions(
            name='datosarchivo',
            options={'verbose_name': 'Datos de XML en PKT SAT', 'verbose_name_plural': 'Datos de XML en PKT SAT'},
        ),
        migrations.AlterModelOptions(
            name='datoslog',
            options={'verbose_name': 'Log datos SAT con Error', 'verbose_name_plural': 'Log datos SAT con Error'},
        ),
        migrations.AlterModelOptions(
            name='polizaarchivo',
            options={'verbose_name': 'Archivo de Polizas', 'verbose_name_plural': 'Archivos de Polizas'},
        ),
        migrations.AddField(
            model_name='polizaarchivo',
            name='total_registros_correctos',
            field=models.BigIntegerField(default=1, verbose_name='Total de Polizas correctas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='polizaarchivo',
            name='total_registros_error',
            field=models.BigIntegerField(default=1, verbose_name='Total de Polizas con error'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='polizaarchivo',
            name='total_registros_procesados',
            field=models.BigIntegerField(default=1, verbose_name='Total de Polizas procesadas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procesa',
            name='total_registros_correctos',
            field=models.BigIntegerField(default=1, verbose_name='Total de XML correctos'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procesa',
            name='total_registros_error',
            field=models.BigIntegerField(default=1, verbose_name='Total de XML con error'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='procesa',
            name='total_registros_procesados',
            field=models.BigIntegerField(default=1, verbose_name='Total de XML procesados'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='conteopolizalog',
            name='archivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.datospoliza', verbose_name='Poliza:'),
        ),
        migrations.AlterField(
            model_name='conteopolizalog',
            name='total_error',
            field=models.BigIntegerField(verbose_name='Total de atributos con error:'),
        ),
        migrations.AlterField(
            model_name='conteopolizalog',
            name='total_exito',
            field=models.BigIntegerField(verbose_name='Total de atributos correctos:'),
        ),
        migrations.AlterField(
            model_name='conteopolizalog',
            name='total_procesado',
            field=models.BigIntegerField(verbose_name='Número Factura:'),
        ),
        migrations.AlterField(
            model_name='datosarchivo',
            name='fechaemision',
            field=models.DateTimeField(blank=True, verbose_name='Fecha de Timbrado'),
        ),
        migrations.AlterField(
            model_name='datospoliza',
            name='FECHA_CREO_XML',
            field=models.DateTimeField(blank=True, verbose_name='Fecha de Creación de XML'),
        ),
        migrations.AlterField(
            model_name='datospoliza',
            name='FECHA_EMISION',
            field=models.DateTimeField(blank=True, verbose_name='Fecha de Emmisión'),
        ),
        migrations.AlterField(
            model_name='procesa',
            name='archivo',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip'])], verbose_name='Archivo SAT'),
        ),
        migrations.AlterField(
            model_name='procesa',
            name='fecha',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga'),
        ),
        migrations.DeleteModel(
            name='Comparar_UUID',
        ),
        migrations.DeleteModel(
            name='DiferenciasUUID',
        ),
        migrations.AddField(
            model_name='diferenciasfecha',
            name='field_poliza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Proceso.datospoliza', verbose_name='Registro Poliza:'),
        ),
        migrations.AddField(
            model_name='diferenciasfecha',
            name='field_sat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Proceso.datosarchivo', verbose_name='Registro SAT:'),
        ),
        migrations.AddField(
            model_name='diferencias',
            name='field_poliza',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Proceso.datospoliza', verbose_name='Registro Poliza:'),
        ),
        migrations.AddField(
            model_name='diferencias',
            name='field_sat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Proceso.datosarchivo', verbose_name='Registro SAT:'),
        ),
        migrations.AddField(
            model_name='conteoxmllog',
            name='archivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.datosarchivo', verbose_name='Archivo:'),
        ),
        migrations.AddField(
            model_name='compararporfecha',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.empresa', verbose_name='Empresa'),
        ),
        migrations.AddField(
            model_name='comparararchivos',
            name='archivo_poliza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.polizaarchivo', verbose_name='Archivo Poliza:'),
        ),
        migrations.AddField(
            model_name='comparararchivos',
            name='archivo_sat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.procesa', verbose_name='Archivo SAT:'),
        ),
        migrations.AddField(
            model_name='cifrascomparacionfecha',
            name='fechas_comparacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.compararporfecha', verbose_name='Comparacion:'),
        ),
        migrations.AddField(
            model_name='cifrascomparacion',
            name='archivos_comparados',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.comparararchivos', verbose_name='Comparacion:'),
        ),
    ]