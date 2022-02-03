# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 22 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = "res.partner"

    nif = fields.Char(string="NIF")
    stat = fields.Char(string="STAT")
    cif = fields.Char(string="CIF")
    rcs = fields.Char(string="RCS")
    date_issue = fields.Date(string="Date of Issue")