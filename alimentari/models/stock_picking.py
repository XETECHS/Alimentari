# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class StockPicking(models.Model):
    _inherit = "stock.picking"
    container=fields.Char('Contenedor',related='purchase_id.container',readonly=True)
    # date_done = fields.Datetime('Date of Transfer', copy=False, readonly=True, help="Date at which the transfer has been processed or cancelled.")



    # def _action_done(self):
    #     """Call `_action_done` on the `stock.move` of the `stock.picking` in `self`.
    #     This method makes sure every `stock.move.line` is linked to a `stock.move` by either
    #     linking them to an existing one or a newly created one.

    #     If the context key `cancel_backorder` is present, backorders won't be created.

    #     :return: True
    #     :rtype: bool
    #     """
    #     self._check_company()

    #     todo_moves = self.mapped('move_lines').filtered(lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
    #     for picking in self:
    #         if picking.owner_id:
    #             picking.move_lines.write({'restrict_partner_id': picking.owner_id.id})
    #             picking.move_line_ids.write({'owner_id': picking.owner_id.id})
    #     todo_moves._action_done(cancel_backorder=self.env.context.get('cancel_backorder'))
    #     self.write({'date_done': self.scheduled_date, 'priority': '0'})

    #     # if incoming moves make other confirmed/partially_available moves available, assign them
    #     done_incoming_moves = self.filtered(lambda p: p.picking_type_id.code == 'incoming').move_lines.filtered(lambda m: m.state == 'done')
    #     done_incoming_moves._trigger_assign()

    #     self._send_confirmation_email()
    #     return True

    



    


