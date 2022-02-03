# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 19 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    ticket_number = fields.Char(string="Ticket Number")
    journey = fields.Char(string="Journey")
    custom_descri = fields.Char(string="Custom Description")

    # def compute_name(self):
    #     # self.name = "\n".join([str(self.ticket_number), str(self.journey), str(self.custom_descri), str(self.name)])
    #     name = []
    #     if self.passenger:
    #         name.append(self.passenger)
    #     if self.ticket_number:
    #         name.append(self.ticket_number)
    #     if self.journey:
    #         name.append(self.journey)
    #     if self.name:
    #         name.append(self.name)
    #     self.name = "\n".join(name)

    @api.onchange('passenger')
    def onchange_passenger(self):
        # self.name = "\n".join([str(self.ticket_number), str(self.journey), str(self.custom_descri), str(self.name)])
        name = []
        if self.passenger:
            name.append(self.passenger)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.journey:
            name.append(self.journey)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = "\n".join(name)

    @api.onchange('ticket_number')
    def onchange_ticket_number(self):
        # self.name = "\n".join([str(self.ticket_number), str(self.journey), str(self.custom_descri), str(self.name)])
        name = []
        if self.passenger:
            name.append(self.passenger)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.journey:
            name.append(self.journey)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = "\n".join(name)

    @api.onchange('journey')
    def onchange_journey(self):
        # self.name = "\n".join([str(self.ticket_number), str(self.journey), str(self.custom_descri), str(self.name)])
        name = []
        if self.passenger:
            name.append(self.passenger)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.journey:
            name.append(self.journey)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = "\n".join(name)

    @api.onchange('custom_descri')
    def onchange_custom_descri(self):
        # self.name = "\n".join([str(self.ticket_number), str(self.journey), str(self.custom_descri), str(self.name)])
        name = []
        if self.passenger:
            name.append(self.passenger)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.journey:
            name.append(self.journey)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = "\n".join(name)