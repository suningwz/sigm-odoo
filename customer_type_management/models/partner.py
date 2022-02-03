# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection([
        ('account', 'Customer account'),
        ('passing', 'Passing customer')
    ], string="Customer Type", default="passing")