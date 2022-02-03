# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 19 May 2021                                         #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

import ftplib
import os
import json
from cryptography.fernet import Fernet
from io import BytesIO

class ResPartner(models.Model):
    _inherit = "res.partner"
    id_hfsql = fields.Char(String="ID HFSQL")

    def import_from_ftp(self):
        __dir__ = os.path.dirname(__file__)

        static_folder_path = os.path.join(os.path.dirname(__dir__), "static")
        log_filename = "server.log"
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

            filename = 'contacts.json'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)

            contacts_data = json.load(byte)

            for row in contacts_data:
                id_hfsql = ('c' if row['type'] == 'customer' else 's') + str(row['contactID'])
                record = self.search([('id_hfsql', '=', id_hfsql)])

                streets = str(row['address']).split("\n")
                street = None
                street2 = None
                try :
                    street = streets[0]
                except Exception as e :
                    street = ""

                try :
                    street2 = streets[1]
                except Exception as e :
                    street2 = ""

                try :
                    country_name = row['country'][0].upper() +row['country'][1:].lower()
                except Exception as e :
                    country_name = ""

                contact = {
                    'name' : row['name'],
                    # 'is_company' : row['cl_type'] == 2,
                    'mobile' : row['phone'],
                    'email' : row['email'],
                    'street' : street,
                    'street2' : street2,
                    'city' : row['ville'],
                    'country_id': self.env['res.country'].search([('name', '=', country_name)]).id,
                    'is_company': row['company_type'] == 1,
                    'customer_rank' : int(row['type'] == 'customer'),
                    'supplier_rank' : int(row['type'] == 'supplier')
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
                    contact['id_hfsql'] = id_hfsql
                    self.create(contact)


        else:
            raise UserError('Unable to connect to the ftp server')