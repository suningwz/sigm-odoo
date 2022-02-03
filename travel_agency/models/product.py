# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 09 December 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    used_for = fields.Selection([
        ('amadeus', "Amadeus"),
        ('to', "Tour Operator"),
        ('both', "Amadeus & Tour Operator")
    ], default='both', string="Used For")

    display_in_invoice_report = fields.Boolean(string="Display in invoice report", default=True)

class ProductProduct(models.Model):
    _inherit = "product.product"
    active_product = fields.Boolean(default=True)