# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):

    _inherit = "res.partner"
    no_g = fields.Char(string="No G")