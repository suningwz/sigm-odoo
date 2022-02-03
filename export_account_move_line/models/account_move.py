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

class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def export_into_ftp(self):
        __dir__ = os.path.dirname(__file__)

        static_folder_path = os.path.join(os.path.dirname(__dir__), "static")

        # ---------------------------------------------------------------------------------------------
        #                                       Get data from query                                   #
        # ---------------------------------------------------------------------------------------------
        query = """
            SELECT
                aml.id ,
                aml.date ,
                aml.move_name ,
                aa.code ,
                aj.name ,
                aml.name ,
                aml.price_total,
                CASE WHEN rp.in_group = True THEN 'C10' ELSE 'C5' END
            FROM account_move_line aml
            INNER JOIN account_move am 
            ON am.id = aml.move_id
            INNER JOIN account_account aa 
            ON aa.id = aml.account_id
            INNER JOIN account_journal aj 
            ON aj.id = aml.journal_id
            INNER JOIN res_partner rp
            ON rp.id = am.partner_id;
        """

        self.env.cr.execute(query)
        data = self.env.cr.fetchall()

        # df = pd.DataFrame(data, columns=['ID', 'Libellé', 'Numéro', 'Date', 'Journal', 'Société', 'Débit', 'Crédit', 'Balance', 'Client/Fournisseur'])
        df = pd.DataFrame(data, columns=['N° Séquence', 'Date Compta.', 'N° Document', 'N° compte général', 'Type origine', 'Désignation', 'Montant', 'Groupe compta. marché'])
        # df.to_csv(static_folder_path + "/CSV/account_move_line.csv", sep=';')
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

        # Sending the file
        session.storbinary('STOR account_move_line.csv', bio)