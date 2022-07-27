# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
import odoo.addons.decimal_precision as dp

class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_alcoholic = fields.Boolean('Es un producto alcoholico?')

class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_order_ext = fields.Char(string='Orden de Compra', size=25) #states={'draft': [('readonly', False)]},)
    
    ref_container = fields.Char(string='No. Contenedor', size=50)
    
    container = fields.Char(string='Contenedor',related='purchase_id.container', readonly=True)
    has_alcohol_products = fields.Boolean('Contiene productos alcoholicos', compute="_has_alcohol_products")
    has_alcohol_products_2 = fields.Boolean('Contiene productos alcoholicos')

    def _has_alcohol_products(self):
        for data in self:
            data.has_alcohol_products = False
            data.has_alcohol_products_2 = False
            if True in data.invoice_line_ids.mapped('product_id.categ_id.is_alcoholic'):
                data.has_alcohol_products = True
                data.has_alcohol_products_2 = True






