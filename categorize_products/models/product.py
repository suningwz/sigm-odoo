# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    category = fields.Selection(
        [
            ('ticket', 'Ticket'),
            ('fees', 'Fees'),
            ('voucher', 'Voucher')
        ],
        string="Product Category"
    )