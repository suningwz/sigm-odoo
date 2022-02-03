# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 09 December 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _

class ResDay(models.Model):
    _name = 'res.day'
    _description = "Day"

    name = fields.Char(string="Name")