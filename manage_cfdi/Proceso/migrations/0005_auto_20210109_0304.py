# Generated by Django 2.2 on 2021-01-09 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Proceso', '0004_comparar_uuid_diferenciasuuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='procesa',
            name='fecha',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha / Hora de carga:'),
        ),
        migrations.AlterField(
            model_name='datosarchivo',
            name='identificador_pkt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proceso.Procesa', verbose_name='Identificador del Paquete'),
        ),
        migrations.AlterField(
            model_name='procesa',
            name='archivo',
            field=models.FileField(upload_to='', verbose_name='Archivo SAT'),
        ),
    ]
