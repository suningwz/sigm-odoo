# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    in_group_account = fields.Many2one('account.account', string="Group Account", default=False)
    out_group_account = fields.Many2one('account.account', string="Out of Group Account", default=False)