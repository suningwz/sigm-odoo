# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 25 Septembre 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

import ftplib
import os
import pandas as pd
import json
from cryptography.fernet import Fernet
from io import BytesIO

class TravelOrder(models.Model):
    _inherit = "travel.order"

    show_confirm_button = fields.Boolean(store=False, compute="_get_button_display_mode")
    button_to_show = fields.Selection(['none', 'confirm', 'confirm_confirm'], string="Button to show", store=False, compute="_get_button_to_show")

    def _get_button_display_mode(self):
        for record in self:
            # record.show_confirm_button = self.env.user.can_confirm_quotation_even_credit_limit_is_reached and record.partner_id.general_credit >= record.partner_id.credit_limit and record.state == 'accepted'
            record.show_confirm_button = self.env.user.can_confirm_quotation_account_client and record.partner_id.general_credit >= record.partner_id.credit_limit and record.state == 'accepted'

    def _get_button_to_show(self):
        if not self.env.user.can_confirm_quotation:
            self.button_to_show = 'none'
        else:
            if self.partner_id.general_credit < self.partner_id.credit_limit:
                self.button_to_show = 'confirm'
            else:
                self.button_to_show = 'confirm_confirm'


    def action_confirm_confirm(self):
        return super(TravelOrder, self).action_confirm()

    def action_confirm(self):
        if not self.env.user.can_confirm_quotation:
            raise UserError(_("You don't have the right to confirm a quotation"))
        else:
            if self.partner_id.customer_type == 'passing':
                return super(TravelOrder, self).action_confirm()
            else:
                if self.partner_id.general_credit < self.partner_id.credit_limit:
                    return super(TravelOrder, self).action_confirm()
                else:
                    if self.env.user.can_confirm_quotation_account_client:
                        return self.action_confirm_confirm()
                    else:
                        alert_msg = _("Can't confirm this quotation!\n" + \
                                        "* Incadea Credit : %s\n" + \
                                        "* General Credit : %s\n" + \
                                        "* This Credit : %s\n" + \
                                        "* Number of Quotation in Credit : %s\n") % (self.partner_id.incadea_credit, self.partner_id.general_credit, self.amount_total, len(self.search([('partner_id', '=', self.partner_id.id), ('state', '=', 'quotation')]))
                        )
                        raise UserError(alert_msg)

    # def action_confirm(self):
    #     if not self.env.user.can_confirm_quotation:
    #         raise UserError(_("You don't have the right to cancel an order!"))
    #     else:
    #         if not self.env.user.can_confirm_quotation_account_client:
    #             if self.partner_id.general_credit >= self.partner_id.credit_limit:
    #                 alert_msg = _("Can't confirm this quotation!\n" + \
    #                                 "* Incadea Credit : %s\n" + \
    #                                 "* General Credit : %s\n" + \
    #                                 "* This Credit : %s\n" + \
    #                                 "* Number of Quotation in Credit : %s\n") % (self.partner_id.incadea_credit, self.partner_id.general_credit, self.amount_total, len(self.search([('partner_id', '=', self.partner_id.id), ('state', '=', 'quotation')]))
    #                 )
    #                 raise UserError(alert_msg)
    #             else:
    #                 return super(TravelOrder, self).action_confirm()
    #         else:
    #             if self.partner_id.general_credit >= self.partner_id.credit_limit and self.partner_id.customer_type != 'account':
    #                 raise UserError(_("You don't have the right to confirm an account customer's quotation"))
    #             else:
    #                 return super(TravelOrder, self).action_confirm()
                    


    # def action_confirm(self):
    #     if self.partner_id.general_credit >= self.partner_id.credit_limit:
    #         # if not self.env.user.can_confirm_quotation_even_credit_limit_is_reached:
    #         if not self.env.user.can_confirm_quotation_account_client:
    #             alert_msg = _("Can't confirm this quotation!\n" + \
    #                             "* Incadea Credit : %s\n" + \
    #                             "* General Credit : %s\n" + \
    #                             "* This Credit : %s\n" + \
    #                             "* Number of Quotation in Credit : %s\n") % (self.partner_id.incadea_credit, self.partner_id.general_credit, self.amount_total, len(self.search([('partner_id', '=', self.partner_id.id), ('state', '=', 'quotation')]))
    #             )
    #             raise UserError(alert_msg)
    #         else:
    #             if self.partner_id.customer_type == 'passing':
    #                 if self.env.user.can_confirm_quotation_passing_client:
    #                     return super(TravelOrder, self).action_confirm()
    #                 else:
    #                     raise UserError(_("You don't have the right to confirm a passing customer's quotation!"))
    #             elif self.partner_id.customer_type == 'account':
    #                 if self.env.user.can_confirm_quotation_account_client:
    #                     return super(TravelOrder, self).action_confirm()
    #                 else:
    #                     raise UserError(_("You don't have the right to confirm an account customer's quotation!"))
    #     else:
    #         return super(TravelOrder, self).action_confirm()

class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_limit = fields.Float(string="Credit Limit", readonly=True)
    incadea_credit = fields.Float(string="Incadea Credit")
    general_credit = fields.Float(string="General Credit", default=0, compute="_compute_general_credit")

    def _compute_general_credit(self):
        for record in self:
            unpaid_quotes = self.env['travel.order'].search(['&', ('partner_id', '=', record.id), ('state', 'in', ('quotation', 'accepted'))])
            record.general_credit = sum([quote.amount_total for quote in unpaid_quotes]) + record.incadea_credit

    def get_credit_infos(self):
        __dir__ = os.path.dirname(__file__)

        static_folder_path = os.path.join(os.path.dirname(__dir__), "static")
        _KEY_ = b'_Eb-ez6gdiB8bU89Y8cwl9LlGFC_0Mbv1CbLS8qNVio='

        with open(static_folder_path + "/config.json") as json_data_file:
            _CONFIG_ = json.load(json_data_file)

        fernet = Fernet(_KEY_)

        ftp_host = _CONFIG_['ftp']['host']
        ftp_user = _CONFIG_['ftp']['username']
        ftp_pwd = fernet.decrypt(bytes(_CONFIG_['ftp']['password'], 'utf-8')).decode('utf-8')
        folder_source = _CONFIG_['jsonfiles']['source']

        
        # ------------------------------------------------------------------------------------
        # Connection to the ftp
        # ------------------------------------------------------------------------------------
        state, session = False, None

        try:
            session = ftplib.FTP(ftp_host, ftp_user, ftp_pwd)
            state = True
        except Exception as e:
            print("Error : Impossible to connect to the FTP server\n{}".format(e))

        # ------------------------------------------------------------------------------------
        # Retrieving files from the FTP server
        # ------------------------------------------------------------------------------------
        if state:
            session.cwd(folder_source)

            filename = 'incadea_credit.csv'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)

            credits_data = pd.read_csv(byte, encoding='utf-8', sep=';')
            credits_data = credits_data.fillna("")

            byte.close()
            session.quit()

            for index, row in credits_data.iterrows():
                id_incadea = row['customer_id']
                record = self.search([('id_incadea', '=', id_incadea)])

                contact = {
                    'credit_limit' : row['credit_limit'],
                    'incadea_credit' : row['credit_amount'],
                }
                
                if len(record.ids):
                    # Check if there was any modification in the contact
                    change = False
                    for key in contact:
                        if contact[key] != record[key]:
                            change = True


                    # If so, update the contact, do nothing otherwise
                    if change:
                        record.write(contact)
        else:
            raise UserError('Unable to connect to the ftp server')

class ResUsers(models.Model):
    _inherit = "res.users"

    can_confirm_quotation = fields.Boolean(string="Can confirm quotation", default=False)
    # can_confirm_quotation_even_credit_limit_is_reached = fields.Boolean(string="Can confirm quotation even when credit limit is reached", default=False)
    can_confirm_quotation_account_client = fields.Boolean(string="Can confirm quotation of account client", default=False)
    can_confirm_quotation_passing_client = fields.Boolean(string="Can confirm quotation of passing client", default=False)

    @api.onchange('can_confirm_quotation')
    def _set_no_right(self):
        if not self.can_confirm_quotation:
            self.update({
                # 'can_confirm_quotation_even_credit_limit_is_reached' : False,
                'can_confirm_quotation_passing_client' : False,
                'can_confirm_quotation_account_client' : False,
            })

    # @api.onchange('can_confirm_quotation_even_credit_limit_is_reached')
    # def _set_right1(self):
    #     if self.can_confirm_quotation_even_credit_limit_is_reached:
    #         self.update({'can_confirm_quotation' : False})

    @api.onchange('can_confirm_quotation_account_client')
    def _set_right2(self):
        if self.can_confirm_quotation_account_client:
            self.update({
                'can_confirm_quotation' : True,
                # 'can_confirm_quotation_even_credit_limit_is_reached' : True
            })

    @api.onchange('can_confirm_quotation_passing_client')
    def _set_right3(self):
        if self.can_confirm_quotation_passing_client:
            self.update({
                'can_confirm_quotation' : True,
                # 'can_confirm_quotation_even_credit_limit_is_reached' : True,
                'can_confirm_quotation_account_client' : True
            })