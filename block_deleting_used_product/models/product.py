# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
	_inherit = 'product.product'

	def unlink(self):
		raise UserError("deletion blocked")