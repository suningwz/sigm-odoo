# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 03 December 2021                                      #
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

class ResPartner(models.Model):

    _inherit = "res.partner"
    id_supplier_incadea = fields.Char(String="ID Incadea")

    def import_suppliers_from_incadea(self):
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

            filename = 'FOURNISSEURS_INCADEA.csv'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)

            contacts_data = pd.read_csv(byte, encoding='utf-8', sep=';')
            contacts_data = contacts_data.fillna("")

            byte.close()
            session.quit()

            for index, row in contacts_data.iterrows():
                id_supplier_incadea = row['EntryNo_G']
                record = self.search([('id_supplier_incadea', '=', id_supplier_incadea)])

                contact = {
                    # 'no_g' : str(row['No_G']),
                    'name' : row['FirstName_G'] + ' ' + row['LastName_G'],
                    # 'is_company' : row['cl_type'] == 2,
                    'street' : row['Address_G'],
                    'street2' : row['Address2_G'],
                    'city' : row['City_G'],
                    'phone' : row['Contact_G'],
                    'mobile' : row['PhoneNo_G'],
                    'email' : row['EMail_G'],
                    'lang' : 'fr_FR' if row['LanguageCode_G'] == 'FR' else 'en_US' if row['LanguageCode_G'] == 'EN' else '',
                    'in_group' : row['GenBusPostingGroup_G'] == 'C10',
                    'country_id': self.env['res.country'].search([('code', '=', row['CountryCode_G'])]).id,
                    'company_type' : 'company' if row['CustomerType_G'] == 'Société' else 'person',
                    'supplier_rank' : 1
                }
                
                if len(record.ids):
                # if False:
                    # Check if there was any modification in the contact
                    change = False
                    for key in contact:
                        if contact[key] != record[key]:
                            change = True


                    # If so, update the contact, do nothing otherwise
                    if change:
                        record.write(contact)
                else:
                    contact['id_supplier_incadea'] = id_supplier_incadea
                    self.create(contact)
        else:
            raise UserError('Unable to connect to the ftp server')