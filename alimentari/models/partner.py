# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def default_account_receivable(self):
        account = self.env['account.account'].search([('code', '=', '11201001')], limit=1)
        if len(account) > 0:
            return account
        else:
            return False

    def default_account_payable(self):
        account = self.env['account.account'].search([('code', '=', '21101001')], limit=1)
        if len(account) > 0:
            return account
        else:
            return False

    property_account_receivable_id = fields.Many2one(default=default_account_receivable)
    property_account_payable_id = fields.Many2one(default=default_account_payable)