# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 23 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
	_inherit = 'account.move'

	global_label = fields.Char(string="Global Label", compute="_get_global_label", required=True)

	def _get_global_label(self):
		for record in self:
			# linked_sale = self.env['sale.order'].search([('name', '=', record.invoice_origin)])
			linked_sale = self.env['travel.order'].search([('name', '=', record.invoice_origin)])

			if linked_sale.id:
				record.global_label = linked_sale.global_label
			else:
				record.global_label = ""


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	global_label = fields.Char(string="Global Label", required=True)