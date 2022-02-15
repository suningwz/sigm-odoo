# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
	_inherit = "account.move.line"

	side_account = fields.Char(string="Side Account", compute="_compute_side_account")

	def _compute_side_account(self):
		for record in self:
			record.side_account = ('cl' if record.partner_id.customer_rank else 'fr' if record.partner_id.supplier_rank else '_') + str(record.partner_id.id)