# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dbm.ndbm import library
from itertools import groupby
from datetime import datetime, timedelta
from math import prod

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    unit_to_box = fields.Float('Cajas', compute='_compute_boxes',store=True)
    complemento = fields.Float('Unidades', compute='_compute_boxes',store=True)

    @api.depends('qty_available')
    def _compute_boxes(self):
        for product in self:
            unidades=product.uom_po_id.factor_inv
            a_mano= product.qty_available
            residuo=a_mano%unidades
            # print("uom_type",product.uom_id.uom_type,product.uom_po_id.uom_type)
            if product.uom_po_id.uom_type =="bigger":
                if residuo ==0:
                    product.unit_to_box=a_mano/unidades
                    product.complemento=0
                    # print("Cajas: ",a_mano/unidades, " residuo: ",0)
                else:
                    product.unit_to_box=a_mano//unidades
                    product.complemento=residuo
                    # print("Cajas: ",a_mano//unidades, " residuo: ",residuo)
            else:
                product.unit_to_box=0
                product.complemento=0
    
    def asignar_tax_y_uom(self):
        #Esta función asignará el impuesto y la unidad de medida a los productos 
        #que no tienen una unidad de medida asignada correctamente y no tienen impuesto
        cont=0
        product_emplate=self.env['product.template'].search([])
        iva_por_pagar= self.env.ref('l10n_gt.1_impuestos_plantilla_iva_por_pagar')
        bebidas_alcoholicas= self.env.ref('__export__.account_tax_3_0da8763b')
        unidad=self.env.ref('uom.product_uom_unit')
        libra=self.env.ref('uom.product_uom_lb')

        con_movimiento=[]
        exitosos=0
        error=0
        for product in product_emplate:
            impuestos=[]
            cont+=1
            for tax in product.taxes_id:
                if tax.id not in impuestos:
                    if tax.id==bebidas_alcoholicas.id:
                        impuestos.append(tax.id)
                        impuestos.append(iva_por_pagar.id)

            if impuestos==[]:
                impuestos.append(iva_por_pagar.id)

            try:
                exitosos+=1
                product.taxes_id=impuestos
                if product.uom_id != libra:
                    product.uom_id=unidad.id
            except:
                error+=1
                if product.id not in con_movimiento:
                    con_movimiento.append(product.id)
            print("producto: {} Impuestos: {}".format(product.name,impuestos))
        
        print("exitosos: ",exitosos," error: ",error)
        print("movimientos: ",con_movimiento)



    


