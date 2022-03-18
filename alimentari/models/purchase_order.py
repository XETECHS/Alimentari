# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from email.policy import default
from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    container=fields.Char('Contenedor', size=65, readonly=True, states={'draft': [('readonly', False)]})
    eta = fields.Date('ETA',  readonly=True, states={'draft': [('readonly', False)]}, default=fields.Datetime.now)
    etd = fields.Date('ETD',  readonly=True, states={'draft': [('readonly', False)]}, default=fields.Datetime.now)