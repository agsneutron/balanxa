# Generated by Django 2.2 on 2021-01-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosArchivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador_archivo', models.CharField(blank=True, max_length=200, verbose_name='Identificador del archivo')),
                ('identificador_pkt', models.CharField(blank=True, max_length=200, verbose_name='Identificador del paquete')),
                ('uuid', models.CharField(blank=True, max_length=200, verbose_name='UUID')),
                ('folio', models.CharField(blank=True, max_length=200, verbose_name='Folio')),
                ('rfc', models.CharField(blank=True, max_length=200, verbose_name='RFC')),
                ('emisornombre', models.CharField(blank=True, max_length=200, verbose_name='Nombre emisor')),
                ('emisorrfc', models.CharField(blank=True, max_length=200, verbose_name='RFC emisor')),
                ('receptornombre', models.CharField(blank=True, max_length=200, verbose_name='Nombre receptor')),
                ('receptorrfc', models.CharField(blank=True, max_length=200, verbose_name='RFC receptor')),
                ('subtotal', models.CharField(blank=True, max_length=200, verbose_name='Subtotal')),
                ('total', models.CharField(blank=True, max_length=200, verbose_name='Total')),
                ('fechaemision', models.CharField(blank=True, max_length=200, verbose_name='Fecha de Timbrado')),
                ('estatus', models.CharField(blank=True, max_length=200, verbose_name='Estatus')),
            ],
            options={
                'verbose_name': 'Datos del Archivo',
                'verbose_name_plural': 'Datos de los Archivos',
            },
        ),
        migrations.CreateModel(
            name='DatosLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador_archivo', models.CharField(blank=True, max_length=200, verbose_name='Identificador del archivo')),
                ('identificador_pkt', models.CharField(blank=True, max_length=200, verbose_name='Identificador del paquete')),
                ('atributo', models.CharField(blank=True, max_length=200, verbose_name='Atributo')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Log',
            },
        ),
        migrations.CreateModel(
            name='Procesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='', verbose_name='Archivo')),
            ],
            options={
                'verbose_name': 'Archivo',
                'verbose_name_plural': 'Archivos',
            },
        ),
    ]