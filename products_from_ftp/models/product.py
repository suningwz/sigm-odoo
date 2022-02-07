# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 31 May 2021                                         #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

import ftplib
import os
import json
from cryptography.fernet import Fernet
from io import BytesIO

class ProductTemplate(models.Model):

    _inherit = "product.template"

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
        #                                Connection to the ftp                               #
        # ------------------------------------------------------------------------------------
        state, session = False, None

        try:
            session = ftplib.FTP(ftp_host, ftp_user, ftp_pwd)
            state = True
        except Exception as e:
            print("Error : Impossible to connect to the FTP server\n{}".format(e))

        # ------------------------------------------------------------------------------------
        #                          Retrieving files from the FTP server                       #
        # ------------------------------------------------------------------------------------

        if state:
            session.cwd(folder_source)

            filename = 'products.json'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)

            products_data = json.load(byte)

            session.quit()

        # ------------------------------------------------------------------------------------
        #                            Import Products from csv file                           #
        # ------------------------------------------------------------------------------------
        for row in products_data:
            id_hfsql = str(row['id'])
            record = self.search([('id_hfsql', '=', id_hfsql)])

            product = {
                'id_hfsql' : id_hfsql,
                'name' : row['name'],
                'used_for' : 'to',
                'type' : 'service',
            }
            
            if len(record.ids):
                # Check if there was any modification in the product
                change = False
                for key in product:
                    if product[key] != record[key]:
                        change = True

                # If so, update the product, do nothing otherwise
                if change:
                    record.write(product)
            else:
                product['id_hfsql'] = id_hfsql
                self.create(product)

    comission = fields.Float(string="Commission")
    id_hfsql = fields.Char(String="ID HFSQL")