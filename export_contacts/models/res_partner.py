# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 11 June 2021                                        #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

import ftplib
import os
import pandas as pd
import json
from cryptography.fernet import Fernet
from io import StringIO
from io import BytesIO

class ResPartner(models.Model):

    _inherit = "res.partner"

    def export_into_ftp(self):
        __dir__ = os.path.dirname(__file__)

        static_folder_path = os.path.join(os.path.dirname(__dir__), "static")

        # ---------------------------------------------------------------------------------------------
        #                                       Get data from query                                   #
        # ---------------------------------------------------------------------------------------------
        query = """
            SELECT  id,
                    name,
                    mobile,
                    email,
                    REPLACE(street2, '\n', ' '),
                    is_company,
                    customer_rank,
                    supplier_rank
            FROM res_partner
            WHERE supplier_rank = 1
            OR customer_rank = 1;
        """

        self.env.cr.execute(query)
        data = self.env.cr.fetchall()

        df = pd.DataFrame(data, columns=['id', 'name', 'mobile', 'email', 'street2', 'is_company', 'customer_rank', 'supplier_rank'])
        buffer = StringIO()
        df.to_csv(buffer, sep=';', index=False)
        text = buffer.getvalue()
        bio = BytesIO(str.encode(text))

        # ---------------------------------------------------------------------------------------------
        #                      Send the generated CSV file into the FTP server                        #
        # ---------------------------------------------------------------------------------------------

        # Initialization
        _CONFIG_ = None
        _KEY_ = b'_Eb-ez6gdiB8bU89Y8cwl9LlGFC_0Mbv1CbLS8qNVio='
        _PASSWORD_DECRYPTED_ = False

        with open(static_folder_path + "/config.json") as json_data_file:
            _CONFIG_ = json.load(json_data_file)

        fernet = Fernet(_KEY_)

        _CONFIG_['ftp']['password'] = fernet.decrypt(bytes(_CONFIG_['ftp']['password'], 'utf-8'))
        _CONFIG_['ftp']['password'] = _CONFIG_['ftp']['password'].decode('utf-8')

        # Connecting to the FTP Server
        session = ftplib.FTP(_CONFIG_['ftp']['host'], _CONFIG_['ftp']['username'], _CONFIG_['ftp']['password'], timeout=100000)

        # Browsing into the destination folder
        session.cwd(_CONFIG_['csvfiles']['dest'])

        session.storbinary('STOR contacts.csv', bio)