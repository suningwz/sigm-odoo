# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	def unlink(self):
		raise UserError("deletion blocked")