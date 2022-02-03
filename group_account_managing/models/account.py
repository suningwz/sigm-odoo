# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('partner_id')
    def onchange_partner(self):
        for line in self.invoice_line_ids:
            if not line.display_type == 'line_section':
                line.account_id = line.product_id.in_group_account if self.partner_id.in_group and line.product_id.in_group_account else line.product_id.out_group_account if not self.partner_id.in_group and line.product_id.out_group_account else line.product_id.property_account_income_id
            # if self.partner_id.in_group:
            #     line.account_id = line.product_id.in_group_account
            # else:
            #     line.account_id = line.product_id.out_group_account

    @api.model
    def create(self, vals):
        if 'invoice_line_ids' in vals:
            partner = self.env['res.partner'].search([('id', '=', vals['partner_id'])])
            for invoice_line in vals['invoice_line_ids']:
                if not ('display_type' in invoice_line[2] and invoice_line[2]['display_type'] == 'line_section'):
                    product = self.env['product.template'].search([('id', '=', invoice_line[2]['product_id'])])

                    invoice_line[2].update({'account_id' : product.in_group_account.id if partner.in_group and product.in_group_account else product.out_group_account.id if not partner.in_group and product.out_group_account else product.property_account_income_id.id})

        return super(AccountMove, self).create(vals)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange('product_id')
    def onchange_product(self):
        partner = self.move_id.partner_id
        product = self.product_id

        self.account_id = product.in_group_account if partner.in_group and product.in_group_account else product.out_group_account if not partner.in_group and product.out_group_account else product.property_account_income_id
        # if self.move_id.partner_id.in_group:
        #     self.account_id = self.product_id.in_group_account
        # else:
        #     self.account_id = self.product_id.out_group_account

