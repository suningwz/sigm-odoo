# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    other_tax = fields.Float(string="Other Tax", compute="_amount_all")
    amount_tva = fields.Float(string="Amount TVA", compute="_amount_all")

    travel_order_id = fields.Many2one('travel.order', string="Travel Order", readonly=True)

    @api.depends('order_line.price_total', 'order_line.other_tax')
    def _amount_all(self):
        super(PurchaseOrder, self)._amount_all()
        for order in self:
            other_tax = 0.0
            amount_tva = order.amount_total - order.amount_untaxed
            for line in order.order_line:
                other_tax += line.other_tax

            order.update({
                'other_tax' : order.currency_id.round(other_tax),
                'amount_tva' : amount_tva,
                'amount_total' : order.amount_total + order.currency_id.round(other_tax),
            })

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    other_tax = fields.Float(string="Other Tax")

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'other_tax')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self:
            line.update({
                'price_total' : line.price_total + line.other_tax,
            })

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)

        # raise UserError(str(res))
        res.update({'other_tax' : self.other_tax})

        return res