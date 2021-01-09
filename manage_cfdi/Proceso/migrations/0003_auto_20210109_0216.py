# Generated by Django 2.2 on 2021-01-09 02:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proceso', '0002_auto_20210108_2238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datosarchivo',
            options={'verbose_name': 'Datos del PKT SAT', 'verbose_name_plural': 'Datos del PKT SAT'},
        ),
        migrations.AlterModelOptions(
            name='datoslog',
            options={'verbose_name': 'Log datos SAT', 'verbose_name_plural': 'Log datos SAT'},
        ),
        migrations.AlterModelOptions(
            name='datospolizalog',
            options={'verbose_name': 'Log datos Poliza', 'verbose_name_plural': 'Log datos Poliza'},
        ),
        migrations.AlterModelOptions(
            name='polizaarchivo',
            options={'verbose_name': 'Archivo Poliza', 'verbose_name_plural': 'Archivos Polizas'},
        ),
        migrations.AlterModelOptions(
            name='procesa',
            options={'verbose_name': 'Archivo SAT', 'verbose_name_plural': 'Archivos SAT'},
        ),
        migrations.RemoveField(
            model_name='datospoliza',
            name='RAZON_SOCIAL',
        ),
        migrations.RemoveField(
            model_name='datospoliza',
            name='RFC',
        ),
        migrations.AddField(
            model_name='datospoliza',
            name='NOMBRE_EMISOR',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nombre Emisor'),
        ),
        migrations.AddField(
            model_name='datospoliza',
            name='NOMBRE_RECEPTOR',
            field=models.CharField(blank=True, max_length=200, verbose_name='Nombre Rceptor'),
        ),
        migrations.AddField(
            model_name='datospoliza',
            name='RFC_EMISOR',
            field=models.CharField(blank=True, max_length=200, verbose_name='RFC Emisor'),
        ),
        migrations.AddField(
            model_name='datospoliza',
            name='RFC_RECEPTOR',
            field=models.CharField(blank=True, max_length=200, verbose_name='RFC Receptor'),
        ),
        migrations.AlterField(
            model_name='polizaarchivo',
            name='archivo',
            field=models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xls', 'xlsx'])], verbose_name='Archivo'),
        ),
    ]