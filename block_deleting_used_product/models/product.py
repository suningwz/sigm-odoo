# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	def unlink(self):
		for record in self:
			tol = self.env['travel.order.line'].search([('product_id', '=', record.id)])

			if tol:
				documents = []
				for line in tol:
					if line.order_id.name not in documents:
						documents.append(line.order_id.name)
				raise UserError(_("This product is used in the following documents and cannot be deleted:\n%s") % ", ".join(documents))
			else:
				raise UserError("This product can be deleted")
