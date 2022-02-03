# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"

    in_group = fields.Boolean(string="Group")