# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

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
            print("uom_type",product.uom_id.uom_type,product.uom_po_id.uom_type)
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



    


