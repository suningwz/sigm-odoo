# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 19 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

import json

class AccountMove(models.Model):
    _inherit = 'account.move'

    report_printed = fields.Boolean(string="Report has been printed", default=False)

    def action_invoice_print(self):
        res = super(AccountMove, self).action_invoice_print()
        self.report_printed = True
        return res

    def action_invoice_print_duplicata(self):
        return self.env.ref('custom_invoice_report.action_report_invoice_with_band').report_action(self)

    # -------------------------------------------------------------------------
    # For Odoo 15
    # -------------------------------------------------------------------------
    def update_json(self, jsondata):
        jsondata = json.loads(jsondata)
        montant_ht_in_jsondata = False
        montant_ht = None
        if "groups_by_subtotal" in jsondata:
            for key in jsondata["groups_by_subtotal"]:
                for item in jsondata["groups_by_subtotal"][key]:
                    item.update({'tax_group_name' : "TVA"})

                if key == "Montant HT":
                    montant_ht = jsondata["groups_by_subtotal"][key]
                    montant_ht_in_jsondata = True

            jsondata["groups_by_subtotal"].update({"Total HT" : montant_ht})
            if montant_ht_in_jsondata:
                del jsondata["groups_by_subtotal"]["Montant HT"]

        if "subtotals" in jsondata:
            for subtotal in jsondata['subtotals']:
                subtotal.update({'name' : 'Total HT'})

        return jsondata
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # For Odoo 14
    # -------------------------------------------------------------------------
    # def update_TVA_text(self):
    #     updated_data = []
    #     for item in self.amount_by_group:
    #         item = list(item)
    #         item[0] = 'TVA'
    #         item.append(_('Amount Tax'))
    #         item.append(self.other_tax)
    #         item = tuple(item)
    #         updated_data.append(item)
    #     return updated_data
    # -------------------------------------------------------------------------

    def origin_order(self):
        order = self.env['travel.order'].search([('name', '=', self.invoice_origin)])
        return order