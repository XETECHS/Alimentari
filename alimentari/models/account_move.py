# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
import odoo.addons.decimal_precision as dp

class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_order_ext = fields.Char(string='Orden de Compra', size=25) #states={'draft': [('readonly', False)]},)
    
    ref_container = fields.Char(string='No. Contenedor', size=50)
    
    container=fields.Char(string='Contenedor',related='purchase_id.container',readonly=True)




