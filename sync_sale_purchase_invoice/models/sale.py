# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError
from datetime import datetime as dt

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        status = super(SaleOrder, self).action_confirm()

        # Create invoice for the sale order
        sale_invoice = self._create_invoices()
        sale_invoice.action_post()

        # Create invoice for each corresponding purchase
        invoices = {}
        for line in self.order_line:
            if line.supplier:
                if not line.supplier in invoices:
                    invoices[line.supplier] = {
                        'partner_id' : line.supplier.id,
                        'ref' : _("Sale Invoice : %s") % self.name,
                        'move_type' : 'in_invoice',
                        'invoice_date' : dt.strftime(dt.now().date(), '%Y-%m-%d'),
                        'invoice_line_ids' : []
                    }

                invoices[line.supplier]['invoice_line_ids'].append((0,0,{
                    'name' : line.name,
                    'product_id' : line.product_id.id,
                    'quantity' : line.product_uom_qty,
                    'price_unit' : line.price_unit,
                    'tax_ids' : line.tax_id,
                    'other_tax' : line.amount_tax,
                }))

        for partner in invoices:
            purchase_invoice = self.env['account.move'].create(invoices[partner])
            purchase_invoice.action_post()

        return status

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    supplier = fields.Many2one('res.partner', string="Supplier", domain="[('supplier_rank', '=', 1)]")

    @api.onchange('supplier')
    def onchange_supplier(self):
        if not self.supplier.supplier_rank:
            self.supplier.write({'supplier_rank' : 1})