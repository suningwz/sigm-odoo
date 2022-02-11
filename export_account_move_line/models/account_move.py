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
        # query = """
        #     SELECT
        #         aml.id ,
        #         aml.date ,
        #         aml.move_name ,
        #         aa.code ,
        #         aj.name ,
        #         aml.name ,
        #         aml.balance,
        #         aml.balance,
        #         CASE WHEN rp.in_group = True THEN 'C10' ELSE 'C5' END
        #     FROM account_move_line aml
        #     INNER JOIN account_move am 
        #     ON am.id = aml.move_id
        #     INNER JOIN account_account aa 
        #     ON aa.id = aml.account_id
        #     INNER JOIN account_journal aj 
        #     ON aj.id = aml.journal_id
        #     INNER JOIN res_partner rp
        #     ON rp.id = am.partner_id
        #     WHERE am.type like '%_invoice' or am.type like '%_refund';
        # """

        # self.env.cr.execute(query)
        # data = self.env.cr.fetchall()

        # # df = pd.DataFrame(data, columns=['ID', 'Libellé', 'Numéro', 'Date', 'Journal', 'Société', 'Débit', 'Crédit', 'Balance', 'Client/Fournisseur'])
        # df = pd.DataFrame(data, columns=['N° Séquence', 'Date Compta.', 'N° Document', 'N° compte général', 'Type origine', 'Désignation', 'Montant', 'Montant ouvert', 'Groupe compta. marché'])

        # ----------------------------------------------
        # Instead of query
        # ----------------------------------------------
        invoices_id = self.env['account.move'].search([('move_type', 'in', ('in_invoice', 'out_invoice', 'in_refund', 'out_refund'))]).ids
        move_lines = self.env['account.move.line'].search([('move_id', 'in', invoices_id)])

        data = {
            'N° Séquence' : [],
            'Date Compta.' : [],
            'N° Document' : [],
            'N° Doc. externe' : [],
            'N° compte général' : [],
            'Code établ.' : [],
            'Code département' : [],
            'Code marque' : [],
            'Type origine' : [],
            'N° origine' : [],
            'VIN' : [],
            'N° contrat atelier' : [],
            'Désignation' : [],
            'Montant' : [],
            'Montant ouvert' : [],
            'Montant TVA' : [],
            'Type compta. TVA' : [],
            'Groupe compta. marché TVA' : [],
            'Groupe compta. produit TVA' : [],
            'Groupe compta. marché' : [],
            'Groupe compta. produit' : [],
            'Code journal' : [],
            'Code Utilisateur' : [],
        }

        for line in move_lines:
            data['N° Séquence'].append(line.id)
            data['Date Compta.'].append(line.date)
            data['N° Document'].append(line.move_id.name)
            data['N° Doc. externe'].append('')
            data['N° compte général'].append(line.account_id.name)
            data['Code établ.'].append('')
            data['Code département'].append('')
            data['Code marque'].append('')
            data['Type origine'].append(line.journal_id.name)
            data['N° origine'].append('')
            data['VIN'].append('')
            data['N° contrat atelier'].append('')
            data['Désignation'].append(line.name)
            data['Montant'].append(line.balance)
            data['Montant ouvert'].append(line.balance)
            data['Montant TVA'].append(sum(line.price_unit * line.quantity * tax.amount / 100 for tax in line.tax_ids))
            data['Type compta. TVA'].append(', '.join([tax.type_tax_use for tax in line.tax_ids]))
            data['Groupe compta. marché TVA'].append('')
            data['Groupe compta. produit TVA'].append('')
            data['Groupe compta. marché'].append('C10' if line.partner_id.in_group else 'C05')
            data['Groupe compta. produit'].append('')
            data['Code journal'].append(line.journal_id.type)
            data['Code Utilisateur'].append('')
        df = pd.DataFrame(data)
        # ----------------------------------------------


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