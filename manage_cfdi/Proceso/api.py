# coding=utf-8

from django.http import HttpResponse
from django.views.generic import ListView
from xml.dom import minidom
import zipfile
import json
from Proceso.models import Procesa, DatosArchivo, DatosPoliza


class ProcesaArchivo(ListView):
    def get(self, request, *args, **kwargs):
        folio = request.GET.get('id')
        try:
            object = Procesa.objects.get(id=folio)
            json_response = []
            xmlfile = minidom.parse(object.archivo)


            #print('\nFile:')
            #print xmlfile
            #print('\nItems:')
            #print items
            # one specific item attribute
            #print('Item #2 attribute:')
            #print(items[1].attributes['name'].value)

            # estatus,


            #getItem  folio, totales
            items = xmlfile.getElementsByTagName('cfdi:Comprobante')
            # all item attributes
            print('\nComprobante attributes:')
            for item in items:
                print(item.attributes['Folio'].value)
                print(item.attributes['SubTotal'].value)
                print(item.attributes['Total'].value)
                json_response.append(item)

            # getItem  rfc emisor, nombre emisor,
            items = xmlfile.getElementsByTagName('cfdi:Emisor')
            # all item attributes
            print('\nEmisor attributes:')
            for item in items:
                print(item.attributes['Rfc'].value)
                print(item.attributes['Nombre'].value)
                json_response.append(item)

            # getItem  rfc emisor, nombre emisor,
            items = xmlfile.getElementsByTagName('cfdi:Receptor')
            # all item attributes
            print('\nReceptor attributes:')
            for item in items:
                print(item.attributes['Rfc'].value)
                print(item.attributes['Nombre'].value)
                json_response.append(item)

            # getItem uuid, fecha de emision
            items = xmlfile.getElementsByTagName('tfd:TimbreFiscalDigital')
            # all item attributes
            print('\nTimbreFiscalDigital attributes:')
            for item in items:
                print(item.attributes['FechaTimbrado'].value)
                print(item.attributes['UUID'].value)
                json_response.append(item)

            return HttpResponse(json.dumps(json_response, indent=4, sort_keys=False, ensure_ascii=False),
                                'application/json; charset=utf-8')

        except Exception as e:
            return HttpResponse("Error: " + str(e.message))


class LeeArchivo(ListView):
    def get(self, request, *args, **kwargs):
        folio = request.GET.get('id')
        try:
            object = Procesa.objects.get(id=folio)
            json_response = []
            zf = zipfile.ZipFile(object.archivo, 'r')
            for name in zf.namelist():
                f = zf.open(name)

                xmlfile = minidom.parse(f)

            # print('\nFile:')
            # print xmlfile
            # print('\nItems:')
            # print items
            # one specific item attribute
            # print('Item #2 attribute:')
            # print(items[1].attributes['name'].value)

            # estatus,

            # getItem  folio, totales
                items = xmlfile.getElementsByTagName('cfdi:Comprobante')
                # all item attributes
                print('\nComprobante attributes:')
                for item in items:
                    print(item.attributes['Folio'].value)
                    print(item.attributes['SubTotal'].value)
                    print(item.attributes['Total'].value)
                    json_response.append(item)

                # getItem  rfc emisor, nombre emisor,
                items = xmlfile.getElementsByTagName('cfdi:Emisor')
                # all item attributes
                print('\nEmisor attributes:')
                for item in items:
                    print(item.attributes['Rfc'].value)
                    print(item.attributes['Nombre'].value)
                    json_response.append(item)

                # getItem  rfc emisor, nombre emisor,
                items = xmlfile.getElementsByTagName('cfdi:Receptor')
                # all item attributes
                print('\nReceptor attributes:')
                for item in items:
                    print(item.attributes['Rfc'].value)
                    print(item.attributes['Nombre'].value)
                    json_response.append(item)

                # getItem uuid, fecha de emision
                items = xmlfile.getElementsByTagName('tfd:TimbreFiscalDigital')
                # all item attributes
                print('\nTimbreFiscalDigital attributes:')
                for item in items:
                    print(item.attributes['FechaTimbrado'].value)
                    print(item.attributes['UUID'].value)
                    json_response.append(item)

            return HttpResponse(json.dumps(json_response, indent=4, sort_keys=False, ensure_ascii=False),
                                'application/json; charset=utf-8')

        except Exception as e:
            return HttpResponse("Error: " + str(e.message))


class get_DataSet(ListView):

    def get(self, request, *args, **kwargs):
        p_rfc = request.GET.get('p_rfc')
        p_fecha_inicio = request.GET.get('p_fecha_inicio')
        p_fecha_fin = request.GET.get('p_fecha_fin')
        print("RFC: " + p_rfc)
        print(p_fecha_inicio)
        print(p_fecha_fin)
        response = DatosArchivo.objects.filter(emisorrfc=p_rfc, fechaemision__range=(p_fecha_inicio, p_fecha_fin))
        print(response)
        response = DatosPoliza.objects.filter(RFC_EMISOR=p_rfc, FECHA_CREO_XML__range=(p_fecha_inicio, p_fecha_fin))
        print(response)
        return HttpResponse(response,'application/json; charset=utf-8')