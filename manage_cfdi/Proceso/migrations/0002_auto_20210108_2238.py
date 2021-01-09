# Generated by Django 2.2 on 2021-01-08 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proceso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosPolizaLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador_archivo', models.CharField(blank=True, max_length=200, verbose_name='Identificador del archivo')),
                ('atributo', models.CharField(blank=True, max_length=200, verbose_name='Atributo')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Log',
            },
        ),
        migrations.CreateModel(
            name='PolizaArchivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='', verbose_name='Archivo')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga:')),
            ],
            options={
                'verbose_name': 'Archivo',
                'verbose_name_plural': 'Archivos',
            },
        ),
        migrations.AddField(
            model_name='datosarchivo',
            name='total_impuesto_trasladado',
            field=models.CharField(blank=True, max_length=200, verbose_name='Total Impuestos Trasladados'),
        ),
        migrations.CreateModel(
            name='DatosPoliza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NO_FACTURA', models.CharField(blank=True, max_length=200, verbose_name='No. Factura')),
                ('SERIE', models.CharField(blank=True, max_length=200, verbose_name='Serie')),
                ('RAZON_SOCIAL', models.CharField(blank=True, max_length=200, verbose_name='Razón Social')),
                ('RFC', models.CharField(blank=True, max_length=200, verbose_name='RFC')),
                ('FORMA_PAGO', models.CharField(blank=True, max_length=200, verbose_name='Forma de Pago')),
                ('FECHA_EMISION', models.CharField(blank=True, max_length=200, verbose_name='Fecha de Emmisión')),
                ('TIPO_FACTURA', models.CharField(blank=True, max_length=200, verbose_name='Tipo de Factura')),
                ('TIPO_MONEDA', models.CharField(blank=True, max_length=200, verbose_name='Tipo de Moneda')),
                ('SUBTOTAL', models.CharField(blank=True, max_length=200, verbose_name='Sub Total')),
                ('IVA', models.CharField(blank=True, max_length=200, verbose_name='IVA')),
                ('DESCUENTO', models.CharField(blank=True, max_length=200, verbose_name='Descuento')),
                ('TOTAL', models.CharField(blank=True, max_length=200, verbose_name='Total')),
                ('SALDO', models.CharField(blank=True, max_length=200, verbose_name='Saldo')),
                ('FECHA_CREO_XML', models.CharField(blank=True, max_length=200, verbose_name='Fecha de Creación de XML')),
                ('TIMBRE_UUID', models.CharField(blank=True, max_length=200, verbose_name='Timbre UUID')),
                ('METODO_PAGO', models.CharField(blank=True, max_length=200, verbose_name='Método de Pago')),
                ('ESTATUS', models.CharField(blank=True, max_length=200, verbose_name='Estatus')),
                ('identificador_archivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.PolizaArchivo', verbose_name='Identificador del Archivo')),
            ],
            options={
                'verbose_name': 'Datos de la Poliza',
                'verbose_name_plural': 'Datos de las Polizas',
            },
        ),
        migrations.CreateModel(
            name='ConteoPolizaLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_procesado', models.BigIntegerField(verbose_name='Total de Registros procesados:')),
                ('total_error', models.BigIntegerField(verbose_name='Total de registros con error:')),
                ('total_exito', models.BigIntegerField(verbose_name='Total de registros correctos:')),
                ('fecha', models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga:')),
                ('archivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.PolizaArchivo', verbose_name='Archivo:')),
            ],
            options={
                'verbose_name': 'Log de Registros Procesados',
                'verbose_name_plural': 'Log de Registros PRocesados',
            },
        ),
    ]