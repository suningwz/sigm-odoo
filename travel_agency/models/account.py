# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 09 December 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

from datetime import datetime as dt

from functools import partial
from odoo.tools.misc import formatLang

class AccountMove(models.Model):
    _inherit = 'account.move'

    global_label = fields.Text(string="Global Label", compute="_get_global_label")
    # other_tax = fields.Float(string="Amount Tax", compute="_compute_other_tax")

    def _get_global_label(self):
        for record in self:
            # linked_sale = self.env['sale.order'].search([('name', '=', record.invoice_origin)])
            linked_travel = self.env['travel.order'].search([('name', '=', record.invoice_origin)])

            if linked_travel.id:
                record.global_label = linked_travel.global_label
            else:
                record.global_label = ""


    # @api.depends('invoice_line_ids.other_tax')
    # def _compute_other_tax(self):
    #     for record in self:
    #         other_tax = 0
    #         for line in record.invoice_line_ids:
    #             other_tax += line.other_tax

    #         record.update({'other_tax' : other_tax})

    # @api.depends('other_tax')
    # def _compute_amount(self):
    #     super(AccountMove, self)._compute_amount()
    #     self.amount_total += self.other_tax
    #     self.amount_tax += self.other_tax

    # @api.model
    # def create(self, vals):
    #     raise UserError(str(vals))

    # def action_reverse(self):
    #     invoices = self.search([('invoice_origin', '=', self.invoice_origin), ('id', '!=', self.id), ('move_type', '=', 'in_invoice')])

    #     # --------------------------------------------------------------
    #     # Create Credit Note for Customer invoice
    #     # --------------------------------------------------------------
    #     action = super(AccountMove, self).action_reverse()
    #     # --------------------------------------------------------------

    #     # --------------------------------------------------------------
    #     # Create Credit Note for Supplier invoice
    #     # --------------------------------------------------------------
    #     for invoice in invoices:
    #         _ = invoice.action_reverse()
    #     # --------------------------------------------------------------

    #     # --------------------------------------------------------------
    #     # Make travel order status in quotation
    #     # --------------------------------------------------------------
    #     travel_order = self.env['travel.order'].search([('name', '=', self.invoice_origin)])
    #     travel_order.action_make_quotation()
    #     # --------------------------------------------------------------
    #     return action