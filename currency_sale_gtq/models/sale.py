from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    amount_gtq = fields.Float(string='Total en GTQ',compute='find_amount', store=True)

    @api.depends("amount_total")
    def find_amount(self):
        for this in self:
            if this.amount_total>0:
                price = self.env['res.currency']._compute(this.currency_id,
                                                      this.company_id.currency_id,
                                                      this.amount_total)
                this.update({'amount_gtq':price})
            else:
                price = 0
                this.update({'amount_gtq':price})

