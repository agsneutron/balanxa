# coding=utf-8

from time import gmtime, strftime
from Proceso.models import CifrasComparacion

class Comparaciones:

    class ObtenerSetPorFecha:


    class Compara:
        # def do_Log(self, uuid_sat, uuid_poliza, uuid_sat_value, uuid_poliza_value, diferencia, nivel, id_comparacion,
        #            fuente):
        #
        #     logDato = Diferencias(
        #         field_sat=uuid_sat,
        #         field_poliza=uuid_poliza,
        #         field_sat_value=uuid_sat_value,
        #         field_poliza_value=uuid_poliza_value,
        #         diferencia=diferencia,
        #         nivel_comparacion=nivel,
        #         source=fuente,
        #         comparacion=id_comparacion,
        #     )
        #     logDato.save()

        def Compara(self, setSAT, setPoliza, p_rfc, p_fecha_inicio, p_fecha_fin, objComparar):

            print(p_rfc)
            print(p_fecha_inicio)
            print(p_fecha_fin)
            datos_sat = setSAT
            datos_poliza = setPoliza

            source = ''
            total_registros_sat = 0
            total_registros_poliza = 0

            c_uuid_found_s = 0
            c_uuid_found_p = 0
            uuid_found_s = 0
            uuid_found_p = 0
            uuid_found_s_p = 0
            uuid_not_found_s_p = 0
            uuid_found_p_s = 0
            uuid_not_found_p_s = 0

            c_folio_found_s = 0
            c_folio_found_p = 0
            folio_found_s = 0
            folio_found_p = 0
            folio_found_s_p = 0
            folio_not_found_s_p = 0
            folio_found_p_s = 0
            folio_not_found_p_s = 0

            c_total_found_s = 0
            c_total_found_p = 0
            total_found_s = 0
            total_found_p = 0
            total_found_s_p = 0
            total_found_p_s = 0
            total_not_found_s_p = 0
            total_not_found_p_s = 0

            c_subtotal_found_s = 0
            c_subtotal_found_p = 0
            subtotal_found_s = 0
            subtotal_found_p = 0
            subtotal_found_s_p = 0
            subtotal_found_p_s = 0
            subtotal_not_found_s_p = 0
            subtotal_not_found_p_s = 0

            c_iva_found_s = 0
            c_iva_found_p = 0
            iva_found_s = 0
            iva_found_p = 0
            iva_found_s_p = 0
            iva_found_p_s = 0
            iva_not_found_s_p = 0
            iva_not_found_p_s = 0

            c_rfcemisor_found_s = 0
            c_rfcemisor_found_p = 0
            rfcemisor_found_s = 0
            rfcemisor_found_p = 0
            rfcemisor_found_s_p = 0
            rfcemisor_found_p_s = 0
            rfcemisor_not_found_s_p = 0
            rfcemisor_not_found_p_s = 0

            c_rfcreceptor_found_s = 0
            c_rfcreceptor_found_p = 0
            rfcreceptor_found_s = 0
            rfcreceptor_found_p = 0
            rfcreceptor_found_s_p = 0
            rfcreceptor_found_p_s = 0
            rfcreceptor_not_found_s_p = 0
            rfcreceptor_not_found_p_s = 0

            c_nombreemisor_found_s = 0
            c_nombreemisor_found_p = 0
            nombreemisor_found_s = 0
            nombreemisor_found_p = 0
            nombreemisor_found_s_p = 0
            nombreemisor_found_p_s = 0
            nombreemisor_not_found_s_p = 0
            nombreemisor_not_found_p_s = 0

            c_nombrereceptor_found_s = 0
            c_nombrereceptor_found_p = 0
            nombrereceptor_found_s = 0
            nombrereceptor_found_p = 0
            nombrereceptor_found_s_p = 0
            nombrereceptor_found_p_s = 0
            nombrereceptor_not_found_s_p = 0
            nombrereceptor_not_found_p_s = 0

            if datos_sat:
                # uuid and folio
                for data_s in datos_sat:
                    source = 'SAT'
                    total_registros_sat = len(datos_sat)
                    data_pl = datos_poliza.filter(TIMBRE_UUID=data_s.uuid,
                                                  NO_FACTURA=data_s.folio, )
                    if data_pl:
                        for data_p in data_pl:
                            print(data_p.TIMBRE_UUID)
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_s_p = uuid_found_s_p + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_s_p = uuid_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID',
                                                    'UUID/Folio', objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_s_p = folio_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_s_p = folio_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio',
                                                    'UUID/Folio', objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_s_p = subtotal_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'UUID/Folio', objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio', objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio', objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio', objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_s_p = total_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_s_p = total_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_s_p = iva_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_s_p = iva_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'UUID/Folio', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'UUID/Folio', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor', 'UUID/Folio', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                    else:
                        # not found uuid folio
                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                        self.do_Log(data_s, None, data_s.uuid + '/' + data_s.folio, 'SIN COINCIDENCIAS', 'UUID, Folio',
                                    'UUID/Folio', objComparar, source)

            if datos_poliza:
                for data_p in datos_poliza:
                    source = 'POLIZA'
                    total_registros_poliza = len(datos_poliza)
                    data_st = datos_sat.filter(uuid=data_p.TIMBRE_UUID,
                                               folio=data_p.NO_FACTURA)
                    if data_st:
                        for data_s in data_st:
                            print('data_s')
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_p_s = uuid_found_p_s + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_p_s = uuid_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_p_s = uuid_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID',
                                                    'UUID/Folio',
                                                    objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID/Folio',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_p_s = folio_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_p_s = folio_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio',
                                                    'UUID/Folio',
                                                    objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID/Folio',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_p_s = subtotal_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'UUID/Folio', objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                'UUID/Folio',
                                                objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_p_s = total_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_p_s = total_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID/Folio',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_p_s = iva_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_p_s = iva_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'UUID/Folio', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID/Folio', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'UUID/Folio', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID/Folio', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID/Folio', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID/Folio', objComparar, source)
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'UUID/Folio', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID/Folio', objComparar, source)
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID/Folio', objComparar, source)
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor',
                                                    'UUID/Folio', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID/Folio', objComparar, source)
                                    rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1

                    else:
                        # not found uuid folio
                        uuid_not_found_p_s = uuid_not_found_p_s + 1
                        self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.TIMBRE_UUID + '/' + data_p.NO_FACTURA,
                                    'TIMBRE_UUID/NO_FACTURA', 'UUID/Folio', objComparar, source)

            cifras = CifrasComparacion(
                archivos_comparados=objComparar,
                total_UUID_sat=c_uuid_found_s,
                total_UUID_poliza=c_uuid_found_p,
                total_UUID_sat_poliza=uuid_found_s_p,
                total_UUID_sat_no_poliza=uuid_not_found_s_p,
                total_UUID_poliza_sat=uuid_found_p_s,
                total_UUID_poliza_no_sat=uuid_not_found_p_s,
                total_folio_sat=c_folio_found_s,
                total_folio_poliza=c_folio_found_p,
                total_folio_sat_poliza=folio_found_s_p,
                total_folio_sat_no_poliza=folio_not_found_s_p,
                total_folio_poliza_sat=folio_found_p_s,
                total_folio_poliza_no_sat=folio_not_found_p_s,
                total_total_sat=c_total_found_s,
                total_total_poliza=c_total_found_p,
                total_total_sat_poliza=total_found_s_p,
                total_total_sat_no_poliza=total_not_found_s_p,
                total_total_poliza_sat=total_found_p_s,
                total_total_poliza_no_sat=total_not_found_p_s,
                total_subtotal_sat=c_subtotal_found_s,
                total_subtotal_poliza=c_subtotal_found_p,
                total_subtotal_sat_poliza=subtotal_found_s_p,
                total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
                total_subtotal_poliza_sat=subtotal_found_p_s,
                total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
                total_iva_sat=c_iva_found_s,
                total_iva_poliza=c_iva_found_p,
                total_iva_sat_poliza=iva_found_s_p,
                total_iva_sat_no_poliza=iva_not_found_s_p,
                total_iva_poliza_sat=iva_found_p_s,
                total_iva_poliza_no_sat=iva_not_found_p_s,
                total_rfcemisor_sat=c_rfcemisor_found_s,
                total_rfcemisor_poliza=c_rfcemisor_found_p,
                total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
                total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
                total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
                total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
                total_rfcreceptor_sat=c_rfcreceptor_found_s,
                total_rfcreceptor_poliza=c_rfcreceptor_found_p,
                total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
                total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
                total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
                total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
                total_nombreemisor_sat=c_nombreemisor_found_s,
                total_nombreemisor_poliza=c_nombreemisor_found_p,
                total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
                total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
                total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
                total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
                total_nombrereceptor_sat=c_nombrereceptor_found_s,
                total_nombrereceptor_poliza=c_nombrereceptor_found_p,
                total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
                total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
                total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
                total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
                fecha_proceso=gmtime(),
                registro_comparacion='UUID/Folio',
            )
            cifras.save()

            source = ''
            total_registros_sat = 0
            total_registros_poliza = 0

            c_uuid_found_s = 0
            c_uuid_found_p = 0
            uuid_found_s = 0
            uuid_found_p = 0
            uuid_found_s_p = 0
            uuid_not_found_s_p = 0
            uuid_found_p_s = 0
            uuid_not_found_p_s = 0

            c_folio_found_s = 0
            c_folio_found_p = 0
            folio_found_s = 0
            folio_found_p = 0
            folio_found_s_p = 0
            folio_not_found_s_p = 0
            folio_found_p_s = 0
            folio_not_found_p_s = 0

            c_total_found_s = 0
            c_total_found_p = 0
            total_found_s = 0
            total_found_p = 0
            total_found_s_p = 0
            total_found_p_s = 0
            total_not_found_s_p = 0
            total_not_found_p_s = 0

            c_subtotal_found_s = 0
            c_subtotal_found_p = 0
            subtotal_found_s = 0
            subtotal_found_p = 0
            subtotal_found_s_p = 0
            subtotal_found_p_s = 0
            subtotal_not_found_s_p = 0
            subtotal_not_found_p_s = 0

            c_iva_found_s = 0
            c_iva_found_p = 0
            iva_found_s = 0
            iva_found_p = 0
            iva_found_s_p = 0
            iva_found_p_s = 0
            iva_not_found_s_p = 0
            iva_not_found_p_s = 0

            c_rfcemisor_found_s = 0
            c_rfcemisor_found_p = 0
            rfcemisor_found_s = 0
            rfcemisor_found_p = 0
            rfcemisor_found_s_p = 0
            rfcemisor_found_p_s = 0
            rfcemisor_not_found_s_p = 0
            rfcemisor_not_found_p_s = 0

            c_rfcreceptor_found_s = 0
            c_rfcreceptor_found_p = 0
            rfcreceptor_found_s = 0
            rfcreceptor_found_p = 0
            rfcreceptor_found_s_p = 0
            rfcreceptor_found_p_s = 0
            rfcreceptor_not_found_s_p = 0
            rfcreceptor_not_found_p_s = 0

            c_nombreemisor_found_s = 0
            c_nombreemisor_found_p = 0
            nombreemisor_found_s = 0
            nombreemisor_found_p = 0
            nombreemisor_found_s_p = 0
            nombreemisor_found_p_s = 0
            nombreemisor_not_found_s_p = 0
            nombreemisor_not_found_p_s = 0

            c_nombrereceptor_found_s = 0
            c_nombrereceptor_found_p = 0
            nombrereceptor_found_s = 0
            nombrereceptor_found_p = 0
            nombrereceptor_found_s_p = 0
            nombrereceptor_found_p_s = 0
            nombrereceptor_not_found_s_p = 0
            nombrereceptor_not_found_p_s = 0

            # segunda comparación
            # sólo
            # UUID
            if datos_sat:
                # uuid
                for data_s in datos_sat:
                    source = 'SAT'
                    total_registros_sat = len(datos_sat)
                    data_pl = datos_poliza.filter(TIMBRE_UUID=data_s.uuid, )
                    if data_pl:
                        for data_p in data_pl:
                            print(data_p.TIMBRE_UUID)
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_s_p = uuid_found_s_p + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_s_p = uuid_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                    objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_s_p = folio_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_s_p = folio_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                    objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_s_p = subtotal_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'UUID', objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_s_p = total_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_s_p = total_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_s_p = total_not_found_s_p + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_s_p = iva_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_s_p = iva_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'UUID', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'UUID', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor', 'UUID', objComparar, source)
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'UUID', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'UUID', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor', 'UUID', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                    else:
                        # not found uuid
                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                        self.do_Log(data_s, None, data_s.uuid, 'SIN COINCIDENCIAS', 'UUID', 'UUID', objComparar, source)

            # segunda UUID
            if datos_poliza:
                for data_p in datos_poliza:
                    source = 'POLIZA'
                    total_registros_poliza = len(datos_poliza)
                    data_st = datos_sat.filter(uuid=data_p.TIMBRE_UUID)
                    if data_st:
                        for data_s in data_st:
                            print('data_s')
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_p_s = uuid_found_p_s + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_p_s = uuid_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_p_s = uuid_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                    objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'UUID',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_p_s = folio_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_p_s = folio_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                    objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'UUID',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_p_s = subtotal_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'UUID', objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'UUID',
                                                objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_p_s = total_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_p_s = total_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'UUID',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_p_s = iva_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_p_s = iva_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'UUID', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'UUID', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'UUID', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'UUID', objComparar, source)
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'UUID', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'UUID', objComparar, source)
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'UUID', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'UUID', objComparar, source)
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor',
                                                    'UUID', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'UUID', objComparar, source)
                                    rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1

                    else:
                        # not found uuid folio
                        uuid_not_found_p_s = uuid_not_found_p_s + 1
                        self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.TIMBRE_UUID, 'UUID', 'UUID', objComparar,
                                    source)

            cifras = CifrasComparacion(
                archivos_comparados=objComparar,
                total_UUID_sat=c_uuid_found_s,
                total_UUID_poliza=c_uuid_found_p,
                total_UUID_sat_poliza=uuid_found_s_p,
                total_UUID_sat_no_poliza=uuid_not_found_s_p,
                total_UUID_poliza_sat=uuid_found_p_s,
                total_UUID_poliza_no_sat=uuid_not_found_p_s,
                total_folio_sat=c_folio_found_s,
                total_folio_poliza=c_folio_found_p,
                total_folio_sat_poliza=folio_found_s_p,
                total_folio_sat_no_poliza=folio_not_found_s_p,
                total_folio_poliza_sat=folio_found_p_s,
                total_folio_poliza_no_sat=folio_not_found_p_s,
                total_total_sat=c_total_found_s,
                total_total_poliza=c_total_found_p,
                total_total_sat_poliza=total_found_s_p,
                total_total_sat_no_poliza=total_not_found_s_p,
                total_total_poliza_sat=total_found_p_s,
                total_total_poliza_no_sat=total_not_found_p_s,
                total_subtotal_sat=c_subtotal_found_s,
                total_subtotal_poliza=c_subtotal_found_p,
                total_subtotal_sat_poliza=subtotal_found_s_p,
                total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
                total_subtotal_poliza_sat=subtotal_found_p_s,
                total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
                total_iva_sat=c_iva_found_s,
                total_iva_poliza=c_iva_found_p,
                total_iva_sat_poliza=iva_found_s_p,
                total_iva_sat_no_poliza=iva_not_found_s_p,
                total_iva_poliza_sat=iva_found_p_s,
                total_iva_poliza_no_sat=iva_not_found_p_s,
                total_rfcemisor_sat=c_rfcemisor_found_s,
                total_rfcemisor_poliza=c_rfcemisor_found_p,
                total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
                total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
                total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
                total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
                total_rfcreceptor_sat=c_rfcreceptor_found_s,
                total_rfcreceptor_poliza=c_rfcreceptor_found_p,
                total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
                total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
                total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
                total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
                total_nombreemisor_sat=c_nombreemisor_found_s,
                total_nombreemisor_poliza=c_nombreemisor_found_p,
                total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
                total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
                total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
                total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
                total_nombrereceptor_sat=c_nombrereceptor_found_s,
                total_nombrereceptor_poliza=c_nombrereceptor_found_p,
                total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
                total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
                total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
                total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
                fecha_proceso=gmtime(),
                registro_comparacion='UUID',
            )
            cifras.save()

            source = ''
            total_registros_sat = 0
            total_registros_poliza = 0

            c_uuid_found_s = 0
            c_uuid_found_p = 0
            uuid_found_s = 0
            uuid_found_p = 0
            uuid_found_s_p = 0
            uuid_not_found_s_p = 0
            uuid_found_p_s = 0
            uuid_not_found_p_s = 0

            c_folio_found_s = 0
            c_folio_found_p = 0
            folio_found_s = 0
            folio_found_p = 0
            folio_found_s_p = 0
            folio_not_found_s_p = 0
            folio_found_p_s = 0
            folio_not_found_p_s = 0

            c_total_found_s = 0
            c_total_found_p = 0
            total_found_s = 0
            total_found_p = 0
            total_found_s_p = 0
            total_found_p_s = 0
            total_not_found_s_p = 0
            total_not_found_p_s = 0

            c_subtotal_found_s = 0
            c_subtotal_found_p = 0
            subtotal_found_s = 0
            subtotal_found_p = 0
            subtotal_found_s_p = 0
            subtotal_found_p_s = 0
            subtotal_not_found_s_p = 0
            subtotal_not_found_p_s = 0

            c_iva_found_s = 0
            c_iva_found_p = 0
            iva_found_s = 0
            iva_found_p = 0
            iva_found_s_p = 0
            iva_found_p_s = 0
            iva_not_found_s_p = 0
            iva_not_found_p_s = 0

            c_rfcemisor_found_s = 0
            c_rfcemisor_found_p = 0
            rfcemisor_found_s = 0
            rfcemisor_found_p = 0
            rfcemisor_found_s_p = 0
            rfcemisor_found_p_s = 0
            rfcemisor_not_found_s_p = 0
            rfcemisor_not_found_p_s = 0

            c_rfcreceptor_found_s = 0
            c_rfcreceptor_found_p = 0
            rfcreceptor_found_s = 0
            rfcreceptor_found_p = 0
            rfcreceptor_found_s_p = 0
            rfcreceptor_found_p_s = 0
            rfcreceptor_not_found_s_p = 0
            rfcreceptor_not_found_p_s = 0

            c_nombreemisor_found_s = 0
            c_nombreemisor_found_p = 0
            nombreemisor_found_s = 0
            nombreemisor_found_p = 0
            nombreemisor_found_s_p = 0
            nombreemisor_found_p_s = 0
            nombreemisor_not_found_s_p = 0
            nombreemisor_not_found_p_s = 0

            c_nombrereceptor_found_s = 0
            c_nombrereceptor_found_p = 0
            nombrereceptor_found_s = 0
            nombrereceptor_found_p = 0
            nombrereceptor_found_s_p = 0
            nombrereceptor_found_p_s = 0
            nombrereceptor_not_found_s_p = 0
            nombrereceptor_not_found_p_s = 0

            # tercera comparación
            # sólo
            # Folio
            if datos_sat:
                # folio
                for data_s in datos_sat:
                    source = 'SAT'
                    total_registros_sat = len(datos_sat)
                    data_pl = datos_poliza.filter(NO_FACTURA=data_s.folio, )
                    if data_pl:
                        for data_p in data_pl:
                            print(data_p.TIMBRE_UUID)
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_s_p = uuid_found_s_p + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_s_p = uuid_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                    objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_s_p = uuid_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_s_p = folio_found_s_p + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_s_p = folio_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                    objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_s_p = folio_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_s_p = subtotal_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'FOLIO',
                                                    objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_s_p = subtotal_not_found_s_p + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_s_p = total_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_s_p = total_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar,
                                                source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar,
                                                source)
                                    total_not_found_s_p = total_not_found_s_p + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar,
                                                source)
                                    total_not_found_s_p = total_not_found_s_p + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_s_p = iva_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_s_p = iva_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'FOLIO', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO',
                                                objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO',
                                                objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO',
                                                objComparar, source)
                                    iva_not_found_s_p = iva_not_found_s_p + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_s_p = nombreemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'FOLIO', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_not_found_s_p = nombreemisor_not_found_s_p + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_found_s_p = nombreemisor_found_s_p + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_s_p = rfcemisor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'FOLIO', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO',
                                                objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO',
                                                objComparar, source)
                                    rfcemisor_not_found_s_p = rfcemisor_not_found_s_p + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO',
                                                objComparar, source)
                                    rfcemisor_found_s_p = rfcemisor_found_s_p + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'FOLIO', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_not_found_s_p = nombrereceptor_not_found_s_p + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_found_s_p = nombrereceptor_found_s_p + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor',
                                                    'FOLIO', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_not_found_s_p = rfcreceptor_not_found_s_p + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_found_s_p = rfcreceptor_found_s_p + 1

                    else:
                        # not found uuid folio
                        uuid_not_found_s_p = uuid_not_found_s_p + 1
                        self.do_Log(data_s, None, data_s.uuid, 'SIN COINCIDENCIAS', 'UUID', 'FOLIO', objComparar,
                                    source)

            # tercera folio poliza
            if datos_poliza:
                for data_p in datos_poliza:
                    source = 'POLIZA'
                    total_registros_poliza = len(datos_poliza)
                    data_st = datos_sat.filter(folio=data_p.NO_FACTURA)
                    if data_st:
                        for data_s in data_st:
                            print('data_s')
                            if data_s.uuid == data_p.TIMBRE_UUID and data_s.folio == data_p.NO_FACTURA \
                                    and data_s.emisornombre == data_p.NOMBRE_EMISOR \
                                    and data_s.emisorrfc == data_p.RFC_EMISOR \
                                    and data_s.receptornombre == data_p.NOMBRE_RECEPTOR \
                                    and data_s.receptorrfc == data_p.RFC_RECEPTOR \
                                    and data_s.subtotal == data_p.SUBTOTAL \
                                    and data_s.total == data_p.TOTAL \
                                    and data_s.total_impuesto_trasladado == data_p.IVA and data_s.fechaemision == data_p.FECHA_EMISION:  # estatus
                                print('no dif')
                                uuid_found_p_s = uuid_found_p_s + 1
                            else:
                                # print(comparación uuid)
                                if len(data_s.uuid) == 0:
                                    uuid_found_s = 0
                                else:
                                    uuid_found_s = 1
                                    c_uuid_found_s = c_uuid_found_s + 1
                                if len(data_p.TIMBRE_UUID) == 0:
                                    uuid_found_p = 0
                                else:
                                    uuid_found_p = 1
                                    c_uuid_found_p = c_uuid_found_p + 1

                                if uuid_found_s == 1 and uuid_found_p == 1:
                                    if data_s.uuid.lower() == data_p.TIMBRE_UUID.lower():
                                        # existe coincide
                                        uuid_found_p_s = uuid_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        uuid_not_found_p_s = uuid_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                    objComparar, source)
                                elif uuid_found_s == 1 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 1:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)
                                elif uuid_found_s == 0 and uuid_found_p == 0:
                                    uuid_not_found_p_s = uuid_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.uuid, data_p.TIMBRE_UUID, 'UUID', 'FOLIO',
                                                objComparar, source)

                                # print(comparación folio)
                                if len(data_s.folio) == 0:
                                    folio_found_s = 0
                                else:
                                    folio_found_s = 1
                                    c_folio_found_s = c_folio_found_s + 1

                                if len(data_p.NO_FACTURA) == 0:
                                    folio_found_p = 0
                                else:
                                    folio_found_p = 1
                                    c_folio_found_p = c_folio_found_p + 1

                                if folio_found_s == 1 and folio_found_p == 1:
                                    if data_s.folio.lower() == data_p.NO_FACTURA.lower():
                                        # existe coincide
                                        folio_found_p_s = folio_found_p_s + 1
                                    else:
                                        # existe no coincide, agregar%coincidencia
                                        folio_not_found_p_s = folio_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                    objComparar, source)
                                elif folio_found_s == 1 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 1:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)
                                elif folio_found_s == 0 and folio_found_p == 0:
                                    folio_not_found_p_s = folio_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.folio, data_p.NO_FACTURA, 'Folio', 'FOLIO',
                                                objComparar, source)

                                # print(comparación subtotal, iva, total)
                                # 'subtotal',   'total','total_impuesto_trasladado',
                                #  SUBTOTAL,   TOTAL, IVA,
                                if len(data_s.subtotal) == 0:
                                    subtotal_found_s = 0
                                else:
                                    subtotal_found_s = 1
                                    c_subtotal_found_s = c_subtotal_found_s + 1

                                if len(data_p.SUBTOTAL) == 0:
                                    subtotal_found_p = 0
                                else:
                                    subtotal_found_p = 1
                                    c_subtotal_found_p = c_subtotal_found_p + 1

                                if subtotal_found_s == 1 and subtotal_found_p == 1:
                                    if data_s.subtotal == data_p.SUBTOTAL:
                                        # existe coincide
                                        subtotal_found_p_s = subtotal_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total',
                                                    'FOLIO', objComparar, source)
                                elif subtotal_found_s == 1 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 1:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)
                                elif subtotal_found_s == 0 and subtotal_found_p == 0:
                                    subtotal_not_found_p_s = subtotal_not_found_p_s + 1
                                    self.do_Log(data_s, data_p, data_s.subtotal, data_p.SUBTOTAL, 'Sub Total', 'FOLIO',
                                                objComparar, source)

                                # total
                                if len(data_s.total) == 0:
                                    total_found_s = 0
                                else:
                                    total_found_s = 1
                                    c_total_found_s = c_total_found_s + 1

                                if len(data_p.TOTAL) == 0:
                                    total_found_p = 0
                                else:
                                    total_found_p = 1
                                    c_total_found_p = c_total_found_p + 1

                                if total_found_s == 1 and total_found_p == 1:
                                    if data_s.total == data_p.TOTAL:
                                        # existe coincide
                                        total_found_p_s = total_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coincidencia
                                        total_not_found_p_s = total_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                    objComparar, source)
                                elif total_found_s == 1 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1
                                elif total_found_s == 0 and total_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total, data_p.TOTAL, 'Total', 'FOLIO',
                                                objComparar, source)
                                    total_not_found_p_s = total_not_found_p_s + 1

                                # total_impuesto_trasladado
                                if len(data_s.total_impuesto_trasladado) == 0:
                                    iva_found_s = 0
                                else:
                                    iva_found_s = 1
                                    c_iva_found_s = c_iva_found_s + 1

                                if len(data_p.IVA) == 0:
                                    iva_found_p = 0
                                else:
                                    iva_found_p = 1
                                    c_iva_found_p = c_iva_found_p + 1

                                if iva_found_s == 1 and iva_found_p == 1:
                                    if data_s.total_impuesto_trasladado == data_p.IVA:
                                        # existe coincide
                                        iva_found_p_s = iva_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coincidencia
                                        iva_not_found_p_s = iva_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                    'FOLIO', objComparar, source)
                                elif iva_found_s == 1 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1
                                elif iva_found_s == 0 and iva_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.total_impuesto_trasladado, data_p.IVA, 'IVA',
                                                'FOLIO', objComparar, source)
                                    iva_not_found_p_s = iva_not_found_p_s + 1

                                #  emisor
                                # 'emisornombre','emisorrfc'
                                #  NOMBRE_EMISOR, RFC_EMISOR
                                if len(data_s.emisornombre) == 0:
                                    nombreemisor_found_s = 0
                                else:
                                    nombreemisor_found_s = 1
                                    c_nombreemisor_found_s = c_nombreemisor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombreemisor_found_p = 0
                                else:
                                    nombreemisor_found_p = 1
                                    c_nombreemisor_found_p = c_nombreemisor_found_p + 1

                                if nombreemisor_found_s == 1 and nombreemisor_found_p == 1:
                                    if data_s.emisornombre == data_p.NOMBRE_EMISOR:
                                        # existe coincide
                                        nombreemisor_found_p_s = nombreemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                    'Nombre Emisor', 'FOLIO', objComparar, source)
                                elif nombreemisor_found_s == 1 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_not_found_p_s = nombreemisor_not_found_p_s + 1
                                elif nombreemisor_found_s == 0 and nombreemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisornombre, data_p.NOMBRE_EMISOR,
                                                'Nombre Emisor',
                                                'FOLIO', objComparar, source)
                                    nombreemisor_found_p_s = nombreemisor_found_p_s + 1

                                # rfc emisor
                                if len(data_s.emisorrfc) == 0:
                                    rfcemisor_found_s = 0
                                else:
                                    rfcemisor_found_s = 1
                                    c_rfcemisor_found_s = c_rfcemisor_found_s + 1

                                if len(data_p.RFC_EMISOR) == 0:
                                    rfcemisor_found_p = 0
                                else:
                                    rfcemisor_found_p = 1
                                    c_rfcemisor_found_p = c_rfcemisor_found_p + 1

                                if rfcemisor_found_s == 1 and rfcemisor_found_p == 1:
                                    if data_s.emisorrfc == data_p.RFC_EMISOR:
                                        # existe coincide
                                        rfcemisor_found_p_s = rfcemisor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                    'FOLIO', objComparar, source)
                                elif rfcemisor_found_s == 1 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO', objComparar, source)
                                    rfcemisor_not_found_p_s = rfcemisor_not_found_p_s + 1
                                elif rfcemisor_found_s == 0 and rfcemisor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.emisorrfc, data_p.RFC_EMISOR, 'RFC Emisor',
                                                'FOLIO', objComparar, source)
                                    rfcemisor_found_p_s = rfcemisor_found_p_s + 1

                                # receptor
                                # 'receptornombre','receptorrfc'
                                # NOMBRE_RECEPTOR, RFC_RECEPTOR,
                                if len(data_s.receptornombre) == 0:
                                    nombrereceptor_found_s = 0
                                else:
                                    nombrereceptor_found_s = 1
                                    c_nombrereceptor_found_s = c_nombrereceptor_found_s + 1

                                if len(data_p.NOMBRE_EMISOR) == 0:
                                    nombrereceptor_found_p = 0
                                else:
                                    nombrereceptor_found_p = 1
                                    c_nombrereceptor_found_p = c_nombrereceptor_found_p + 1

                                if nombrereceptor_found_s == 1 and nombrereceptor_found_p == 1:
                                    if data_s.receptornombre == data_p.NOMBRE_RECEPTOR:
                                        # existe coincide
                                        nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1
                                    else:
                                        # existe no coincide  agregar%coicidencia
                                        nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                    'Nombre Receptor', 'FOLIO', objComparar, source)
                                elif nombrereceptor_found_s == 1 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_not_found_p_s = nombrereceptor_not_found_p_s + 1
                                elif nombrereceptor_found_s == 0 and nombrereceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptornombre, data_p.NOMBRE_RECEPTOR,
                                                'Nombre Receptor', 'FOLIO', objComparar, source)
                                    nombrereceptor_found_p_s = nombrereceptor_found_p_s + 1

                                # rfc receptor
                                if len(data_s.receptorrfc) == 0:
                                    rfcreceptor_found_s = 0
                                else:
                                    rfcreceptor_found_s = 1
                                    c_rfcreceptor_found_s = c_rfcreceptor_found_s + 1

                                if len(data_p.RFC_RECEPTOR) == 0:
                                    rfcreceptor_found_p = 0
                                else:
                                    rfcreceptor_found_p = 1
                                    c_rfcreceptor_found_p = c_rfcreceptor_found_p + 1

                                if rfcreceptor_found_s == 1 and rfcreceptor_found_p == 1:
                                    if data_s.receptorrfc == data_p.RFC_RECEPTOR:
                                        # existe coincide
                                        rfcreceptor_found_p_s = rfcreceptor_found_p_s + 1
                                    else:
                                        # existe no coincide agregar%coicidencia
                                        rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                        self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR,
                                                    'RFC Receptor',
                                                    'FOLIO', objComparar, source)
                                elif rfcreceptor_found_s == 1 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 1:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1
                                elif rfcreceptor_found_s == 0 and rfcreceptor_found_p == 0:
                                    self.do_Log(data_s, data_p, data_s.receptorrfc, data_p.RFC_RECEPTOR, 'RFC Receptor',
                                                'FOLIO', objComparar, source)
                                    rfcreceptor_not_found_p_s = rfcreceptor_not_found_p_s + 1

                    else:
                        # not found folio
                        folio_not_found_p_s = folio_not_found_p_s + 1
                        self.do_Log(None, data_p, 'SIN COINCIDENCIAS', data_p.NO_FACTURA, 'Folio', 'FOLIO', objComparar,
                                    source)

            cifras = CifrasComparacion(
                archivos_comparados=objComparar,
                total_UUID_sat=c_uuid_found_s,
                total_UUID_poliza=c_uuid_found_p,
                total_UUID_sat_poliza=uuid_found_s_p,
                total_UUID_sat_no_poliza=uuid_not_found_s_p,
                total_UUID_poliza_sat=uuid_found_p_s,
                total_UUID_poliza_no_sat=uuid_not_found_p_s,
                total_folio_sat=c_folio_found_s,
                total_folio_poliza=c_folio_found_p,
                total_folio_sat_poliza=folio_found_s_p,
                total_folio_sat_no_poliza=folio_not_found_s_p,
                total_folio_poliza_sat=folio_found_p_s,
                total_folio_poliza_no_sat=folio_not_found_p_s,
                total_total_sat=c_total_found_s,
                total_total_poliza=c_total_found_p,
                total_total_sat_poliza=total_found_s_p,
                total_total_sat_no_poliza=total_not_found_s_p,
                total_total_poliza_sat=total_found_p_s,
                total_total_poliza_no_sat=total_not_found_p_s,
                total_subtotal_sat=c_subtotal_found_s,
                total_subtotal_poliza=c_subtotal_found_p,
                total_subtotal_sat_poliza=subtotal_found_s_p,
                total_subtotal_sat_no_poliza=subtotal_not_found_s_p,
                total_subtotal_poliza_sat=subtotal_found_p_s,
                total_subtotal_poliza_no_sat=subtotal_not_found_p_s,
                total_iva_sat=c_iva_found_s,
                total_iva_poliza=c_iva_found_p,
                total_iva_sat_poliza=iva_found_s_p,
                total_iva_sat_no_poliza=iva_not_found_s_p,
                total_iva_poliza_sat=iva_found_p_s,
                total_iva_poliza_no_sat=iva_not_found_p_s,
                total_rfcemisor_sat=c_rfcemisor_found_s,
                total_rfcemisor_poliza=c_rfcemisor_found_p,
                total_rfcemisor_sat_poliza=rfcemisor_found_s_p,
                total_rfcemisor_sat_no_poliza=rfcemisor_not_found_s_p,
                total_rfcemisor_poliza_sat=rfcemisor_found_p_s,
                total_rfcemisor_poliza_no_sat=rfcemisor_not_found_p_s,
                total_rfcreceptor_sat=c_rfcreceptor_found_s,
                total_rfcreceptor_poliza=c_rfcreceptor_found_p,
                total_rfcreceptor_sat_poliza=rfcreceptor_found_s_p,
                total_rfcreceptor_sat_no_poliza=rfcreceptor_not_found_s_p,
                total_rfcreceptor_poliza_sat=rfcreceptor_found_p_s,
                total_rfcreceptor_poliza_no_sat=rfcreceptor_not_found_p_s,
                total_nombreemisor_sat=c_nombreemisor_found_s,
                total_nombreemisor_poliza=c_nombreemisor_found_p,
                total_nombreemisor_sat_poliza=nombreemisor_found_s_p,
                total_nombreemisor_sat_no_poliza=nombreemisor_not_found_s_p,
                total_nombreemisor_poliza_sat=nombreemisor_found_p_s,
                total_nombreemisor_poliza_no_sat=nombreemisor_not_found_p_s,
                total_nombrereceptor_sat=c_nombrereceptor_found_s,
                total_nombrereceptor_poliza=c_nombrereceptor_found_p,
                total_nombrereceptor_sat_poliza=nombrereceptor_found_s_p,
                total_nombrereceptor_sat_no_poliza=nombrereceptor_not_found_s_p,
                total_nombrereceptor_poliza_sat=nombrereceptor_found_p_s,
                total_nombrereceptor_poliza_no_sat=nombrereceptor_not_found_p_s,
                fecha_proceso=gmtime(),
                registro_comparacion='FOLIO',
            )
            cifras.save()

            objComparar.total_registros_sat = total_registros_sat
            objComparar.total_registros_poliza = total_registros_poliza
            objComparar.save(update_fields=['total_registros_sat', 'total_registros_poliza'])
