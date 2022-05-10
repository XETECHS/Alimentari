# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.misc import formatLang


class ReportSaleBook(models.AbstractModel):
    _name = 'report.report_ventas_compras.report_sale_book'

    @api.model
    def _get_report_values(self, docids, data=None):
        company_id = data.get('form', {}).get(
            'company_id', False)
        if not company_id:
            company_id = self.env.user.company_id
        else:
            company_id = self.env['res.company'].browse(company_id[0])
        # Transfrom type date_from
        date_from = data['form']['date_from']
        date_from = date_from.replace('-','/')
        date_from = datetime.strptime(date_from, '%Y/%m/%d')
        # Transfrom type date_to
        date_to = data['form']['date_to']
        date_to = date_to.replace('-','/')
        date_to = datetime.strptime(date_to, '%Y/%m/%d')
        folio = data['form']['folio_inicial']
        folio_inicial = data['form'].get('folio_inicial', 1)
        max_lines_folio = data['form']['max_lines_folio']
        data, ultima = self.generate_records(data, max_lines_folio)
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': model,
            'docs': docs,
            'self': self,
            'data': data,
            'ultima': ultima,
            'format_price': self._format_price,
            'company_id': company_id,
            'date_to': date_to,
            'date_from': date_from,
            'folio_inicial': folio_inicial,
            'max_lines_folio': max_lines_folio
        }
        return docargs

    #@api.multi
    def _format_price(self, price, currency_id):
        if not price:
            return '0.00'
        amount_f = formatLang(self.env, price, dp='Product Price',
                              currency_obj=currency_id)
        amount_f = amount_f.replace(currency_id.symbol, '').strip()
        return amount_f

    #@api.multi
    def generate_records(self, data, max_lines_folio):
        result = []
        if not data.get('form', False):
            return result

        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        total_iva = 0.00
        total_bebidas = 0.00

        #BIENES
        total_bienes_gravados = 0.00
        total_bienes_exentos = 0.00
        total_bienes_iva = 0.00
        total_bienes_bebidas = 0.00
        total_bienes = 0.00
        
        #SERVICIOS
        total_serv_gravados = 0.00
        total_serv_exentos = 0.00
        total_serv_iva = 0.00
        total_serv_bebidas = 0.00

        #EXPORTACIONES
        total_expo_gravados = 0.00
        total_expo_exentos = 0.00
        total_expo_iva = 0.00
        total_expo_bebidas = 0.00
        
        #NC
        total_nc_gravados = 0.00
        total_nc_exentos = 0.00
        total_nc_iva = 0.00
        total_nc_bebidas = 0.00
        total_nc = 0.00
        
        #ND
        total_nd_gravados = 0.00
        total_nd_exentos = 0.00
        total_nd_iva = 0.00
        total_nd_bebidas = 0.00
        total_nd = 0.00

        journal_ids = data['form']['journal_ids']
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        empresa = self.env['res.company'].browse(
            data['form']['company_id'][0])
        folio = data['form']['folio_inicial']
        facturas = self.env['account.move'].search(
            [('state', 'in', ['posted', 'cancel']),
                ('journal_id', 'in', journal_ids),
                ('invoice_date', '>=', date_from),
                ('invoice_date', '<=', date_to),
                ('company_id', '=', empresa.id)], order='id')
        establecimientos = ", ".join([
            jou.name for jou in self.env['account.journal'].browse(
                journal_ids)])

        for inv in facturas:
            bien_local_gravado = 0.00
            servicio_local_gravado = 0.00
            bien_local_exento = 0.00
            servicio_local_exento = 0.00
            bien_expo_gravada = 0.00
            servicio_expo_gravada = 0.00
            bien_expo_exenta = 0.00
            servicio_expo_exento = 0.00

            iva_bien_l = 0.00
            iva_servicio_l = 0.00
            iva_bien_expo = 0.00
            iva_servicio_expo = 0.00
            total_iva = 0.00

            bebidas_bien_l = 0.00
            bebidas_servicio_l = 0.00
            bebidas_bien_expo = 0.00
            bebidas_servicio_expo = 0.00
            total_bebidas = 0.00
            
            # amount_g = 0.00
            # amount_e = 0.00
            # amount_iva = 0.00
            tipo = "FC"
            type_nb = inv.tax_inovice_old
            cad = str(inv.name or '').split('/')
            serie = cad[0]
            numero = cad[0]
            if len(cad) >= 3:
                numero = cad[2]

            if inv.move_type == "out_refund":
                #tipo = 'NC' if inv.amount_untaxed >= 0 else 'ND'
                tipo = 'NC'

            for line in inv.invoice_line_ids:
                precio = line.price_unit if inv.state != 'cancel' else 0.0
                if inv.currency_id != empresa.currency_id:
                    precio = inv.currency_id._convert(precio, empresa.currency_id, empresa, inv.date)
                precio = precio * (1-(line.discount or 0.0)/100.0)
                if tipo == 'NC':
                    precio = precio * -1
                taxes = line.tax_ids.compute_all(
                    precio, empresa.currency_id, line.quantity,
                    line.product_id, inv.partner_id)
                aux_gravado = taxes['total_excluded']
                aux_iva = 0.00
                aux_bebidas = 0.00
                if line.tax_ids:
                    for tax in taxes['taxes']:
                        # aux_iva += tax['amount']
                        if tax['id']!=self.env.ref('__export__.account_tax_3_0da8763b').id:
                            print("IVA", tax['amount'])
                            aux_iva += tax['amount']
                        else:
                            print("BEBIDAS", tax['amount'])
                            aux_bebidas += tax['amount']


                if line.tipo_gasto == "compra":
                    if line.tax_ids or type_nb == "True":
                        bien_local_gravado += aux_gravado
                        iva_bien_l += aux_iva
                        bebidas_bien_l += aux_bebidas
                        if tipo == 'NC':
                            total_nc_gravados += aux_gravado
                            total_nc_iva += aux_iva
                            total_nc_bebidas += aux_bebidas
                        elif tipo == 'ND':
                            total_nd_gravados += aux_gravado
                            total_nd_iva += aux_iva
                            total_nd_bebidas += aux_bebidas
                        else:
                            total_bienes_gravados += aux_gravado
                            total_bienes_iva += aux_iva
                            total_bienes_bebidas += aux_bebidas
                    else:
                        bien_local_exento += aux_gravado
                        if tipo == 'NC':
                            total_nc_exentos += aux_gravado
                        elif tipo == 'ND':
                            total_nd_exentos += aux_gravado
                        else:
                            total_bienes_exentos += aux_gravado
                elif line.tipo_gasto == "servicio":
                    if line.tax_ids  or type_nb == "True":
                        servicio_local_gravado += aux_gravado
                        iva_servicio_l += aux_iva
                        bebidas_servicio_l += aux_bebidas
                        if tipo == 'NC':
                            total_nc_gravados += aux_gravado
                            total_nc_iva += aux_iva
                            total_nc_bebidas += aux_bebidas
                        elif tipo == 'ND':
                            total_nd_gravados += aux_gravado
                            total_nd_iva += aux_iva
                            total_nd_bebidas += aux_bebidas
                        else:
                            total_serv_gravados += aux_gravado
                            total_serv_iva += aux_iva
                            total_serv_bebidas += aux_bebidas
                    else:
                        servicio_local_exento += aux_gravado
                        if tipo == 'NC':
                            total_nc_exentos += aux_gravado
                        elif tipo == 'ND':
                            total_nd_exentos += aux_gravado
                        else:
                            total_serv_exentos += aux_gravado
                elif line.tipo_gasto in ("exportacion", "importacion"):
                    if line.product_id.type == "service":
                        if line.tax_ids or type_nb == "True":
                            servicio_expo_gravada += aux_gravado
                            iva_servicio_expo += aux_iva
                            bebidas_servicio_expo += aux_bebidas
                        else:
                            servicio_expo_exento += aux_gravado
                    else:
                        if line.tax_ids or type_nb == "True":
                            bien_expo_gravada += aux_gravado
                            iva_bien_expo += aux_iva
                            bebidas_bien_expo += aux_bebidas
                        else:
                            bien_expo_exenta += aux_gravado
                    if line.tax_ids or type_nb == "True":
                        if tipo == 'NC':
                            total_nc_gravados += aux_gravado
                            total_nc_iva += aux_iva
                            total_nc_bebidas += aux_bebidas
                        elif tipo == 'ND':
                            total_nd_gravados += aux_gravado
                            total_nd_iva += aux_iva
                            total_nd_bebidas += aux_bebidas
                        else:
                            total_expo_gravados += aux_gravado
                            total_expo_iva += aux_iva
                            total_expo_bebidas += aux_bebidas
                    else:
                        if tipo == 'NC':
                            total_nc_exentos += aux_gravado
                        elif tipo == 'ND':
                            total_nd_exentos += aux_gravado
                        else:
                            total_expo_exentos += aux_gravado

            total_iva = sum([iva_bien_l, iva_servicio_l, iva_bien_expo,
                             iva_servicio_expo])
            total_bebidas = sum([bebidas_bien_l,bebidas_servicio_l,bebidas_bien_expo,bebidas_servicio_expo])
            amount_total = sum([bien_local_gravado, servicio_local_gravado,
                                bien_local_exento, servicio_local_exento,
                                bien_expo_gravada, servicio_expo_gravada,
                                bien_expo_exenta, servicio_expo_exento,
                                total_iva,total_bebidas])
            linea = {
                'company': empresa.name.encode('ascii', 'ignore') or "",
                'nit': empresa.vat or "",
                'direccion': empresa.street.encode('ascii', 'ignore'),
                'folio_no': int(folio),
                'establecimientos': establecimientos,
                # 'mes': mes,
                'fecha': datetime.strptime(
                    str(inv.invoice_date),
                    DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                'tipo': inv.name,
                'serie': inv.fe_serie,
                'numero': inv.fe_number,
                'nit_cliente': inv.partner_id.vat or "C/F",
                'cliente': str(inv.partner_id.name).encode('ascii', 'ignore'),
                'bienes_gravados': bien_local_gravado,
                'servicios_gravados': servicio_local_gravado,
                'bienes_exentos': bien_local_exento,
                'servicios_exentos': servicio_local_exento,
                'bienes_e_gravados': bien_expo_gravada,
                'servicios_e_gravados': servicio_expo_gravada,
                'bienes_e_exentos': bien_expo_exenta,
                'servicios_e_exentos': servicio_expo_exento,
                'iva': total_iva,
                'bebidas': total_bebidas,
                'subtotal': amount_total,
            }
            result.append(linea)
        #SUMATORIAS GENERALES (RESUMEN)
        total_bienes = sum([total_bienes_gravados, total_bienes_exentos,
                            total_bienes_iva,total_bienes_bebidas])
        total_servicios = sum([total_serv_gravados, total_serv_exentos,
                               total_serv_iva,total_serv_bebidas])
        total_nc = sum([total_nc_gravados, total_nc_exentos, total_nc_iva,total_nc_bebidas])
        
        total_nd = sum([total_nd_gravados, total_nd_exentos, total_nd_iva,total_nd_bebidas])
        total_gravado = sum([total_bienes_gravados, total_serv_gravados,
                             total_nc_gravados, total_nd_gravados,
                             total_expo_gravados])
        total_exento = sum([total_bienes_exentos, total_serv_exentos,
                            total_nc_exentos, total_nd_exentos,
                            total_expo_exentos])
        total_imp = sum([total_bienes_iva, total_serv_iva, total_nc_iva,total_nd_iva, total_expo_iva,
                         total_bienes_bebidas, total_serv_bebidas, total_nc_bebidas, total_nd_bebidas, total_expo_bebidas])

        # 'total_gravado': total_gravado,
        # 'total_exento': total_exento,
        # 'total_iva': sum([total_bienes_iva, total_serv_iva, total_nc_iva, total_nd_iva, total_expo_iva]),
        # 'total_bebidas': sum([total_bienes_bebidas, total_serv_bebidas, total_nc_bebidas, total_nd_bebidas, total_expo_bebidas]),
        # 'total_total': sum([total_gravado, total_exento, total_imp])

            
        linea = {
            'cliente': "**Ultima Linea**",
            #BIENES
            'total_bienes_gravados': total_bienes_gravados,
            'total_bienes_exentos': total_bienes_exentos,
            'total_bienes_iva': total_bienes_iva,
            'total_bienes_bebidas': total_bienes_bebidas,
            'total_bienes': total_bienes,
            #SERVICIOS
            'total_servicios_gravados': total_serv_gravados,
            'total_servicios_exentos': total_serv_exentos,
            'total_servicios_iva': total_serv_iva,
            'total_servicios_bebidas': total_serv_bebidas,
            'total_servicios': total_servicios,
            #NC
            'total_nc_gravados': total_nc_gravados,
            'total_nc_exentos': total_nc_exentos,
            'total_nc_iva': total_nc_iva,
            'total_nc_bebidas': total_nc_bebidas,
            'total_nc': total_nc,
            #ND
            'total_nd_gravados': total_nd_gravados,
            'total_nd_exentos': total_nd_exentos,
            'total_nd_iva': total_nd_iva,
            'total_nd_bebidas': total_nd_bebidas,
            'total_nd': total_nd,
            #EXPORTACION
            'total_expo_gravados': total_expo_gravados,
            'total_expo_exentos': total_expo_exentos,
            'total_expo_iva': total_expo_iva,
            'total_expo_bebidas': total_expo_bebidas,
            'total_expor': sum([total_expo_gravados, total_expo_exentos, total_expo_iva,total_expo_bebidas]),
            #TOTALES
            'total_gravado': total_gravado,
            'total_exento': total_exento,
            'total_iva': sum([total_bienes_iva, total_serv_iva, total_nc_iva, total_nd_iva, total_expo_iva]),
            'total_bebidas': sum([total_bienes_bebidas, total_serv_bebidas, total_nc_bebidas, total_nd_bebidas, total_expo_bebidas]),
            'total_total': sum([total_gravado, total_exento, total_imp])
        }
        results = []
        folio = 0
        i = 1
        rows = []
        for row in result:
            rows.append(row)
            if i == max_lines_folio:
                results.append([folio, rows])
                rows = []
                i = 1
                folio += 1
            else:
                i += 1
        if len(rows) > 0:
            results.append([folio, rows])

        return results, linea
