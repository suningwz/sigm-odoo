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
        # Instead of query (based on Ecritures Incadea)
        # ----------------------------------------------
        # invoices_id = self.env['account.move'].search([('move_type', 'in', ('in_invoice', 'out_invoice', 'in_refund', 'out_refund'))]).ids
        # move_lines = self.env['account.move.line'].search([('move_id', 'in', invoices_id)])

        # data = {
        #     'N° Séquence' : [],
        #     'Date Compta.' : [],
        #     'N° Document' : [],
        #     'N° Doc. externe' : [],
        #     'N° compte général' : [],
        #     'Code établ.' : [],
        #     'Code département' : [],
        #     'Code marque' : [],
        #     'Type origine' : [],
        #     'N° origine' : [],
        #     'VIN' : [],
        #     'N° contrat atelier' : [],
        #     'Désignation' : [],
        #     'Montant' : [],
        #     'Montant ouvert' : [],
        #     'Montant TVA' : [],
        #     'Type compta. TVA' : [],
        #     'Groupe compta. marché TVA' : [],
        #     'Groupe compta. produit TVA' : [],
        #     'Groupe compta. marché' : [],
        #     'Groupe compta. produit' : [],
        #     'Code journal' : [],
        #     'Code Utilisateur' : [],
        # }

        # for line in move_lines:
        #     data['N° Séquence'].append(line.id)
        #     data['Date Compta.'].append(line.date)
        #     data['N° Document'].append(line.move_id.name)
        #     data['N° Doc. externe'].append('')
        #     data['N° compte général'].append(line.account_id.name)
        #     data['Code établ.'].append('')
        #     data['Code département'].append('')
        #     data['Code marque'].append('')
        #     data['Type origine'].append(line.journal_id.name)
        #     data['N° origine'].append('')
        #     data['VIN'].append('')
        #     data['N° contrat atelier'].append('')
        #     data['Désignation'].append(line.name)
        #     data['Montant'].append(line.balance)
        #     data['Montant ouvert'].append(line.balance)
        #     data['Montant TVA'].append(sum(line.price_unit * line.quantity * tax.amount / 100 for tax in line.tax_ids))
        #     data['Type compta. TVA'].append(', '.join([tax.type_tax_use for tax in line.tax_ids]))
        #     data['Groupe compta. marché TVA'].append('')
        #     data['Groupe compta. produit TVA'].append('')
        #     data['Groupe compta. marché'].append('C10' if line.partner_id.in_group else 'C05')
        #     data['Groupe compta. produit'].append('')
        #     data['Code journal'].append(line.journal_id.type)
        #     data['Code Utilisateur'].append('')
        # df = pd.DataFrame(data)
        # ----------------------------------------------

        # -------------------------------------------------------
        # Instead of query (based on Ecritures LOCPRO Attendues)
        # -------------------------------------------------------
        invoices_id = self.env['account.move'].search([('move_type', 'in', ('in_invoice', 'out_invoice', 'in_refund', 'out_refund'))]).ids
        move_lines = self.env['account.move.line'].search([('move_id', 'in', invoices_id)])

        data = {
            'Journal Template Name' : ['Nom modèle feuille'],
            'Line No.' : ['N° ligne'],
            'Account Type' : ['Type compte'],
            'Account No.' : ['N° compte'],
            'Posting Date' : ['Date comptabilisation'],
            'Document Type' : ['Type document'],
            'Document No.' : ['N° Document'],
            'Description' : ['Désignation'],
            'VAT%' : ['%TVA'],
            'Currency Code' : ['Code devise'],
            'Amount' : ['Montant'],
            'Amount(LCY)' : ['Montant DS'],
            'Currency Factor' : ['Facteur devise'],
            'Inv. Discount(LCY)' : ['Remises facture DS'],
            'Sell-to/Buy-from No.' : ["N° Donneur/Preneur d'ordre"],
            'Posting Group' : ['Groupe comptabilisation'],
            'Department Code' : ['Code département'],
            'Make Code' : ['Code marque'],
            'Salepers./Purch. Code' : ['Code vendeur/acheteur'],
            'Source Code' : ['Code journal'],
            'System-Created Entry' : ['Ecriture système'],
            'Due Date' : ["Date d'échéance"],
            'Journal Batch Name' : ['Nom feuille'],
            'Posting Type' : ['Type comptabilisation'],
            'Document Date' : ['Date document'],
            'External Document No.' : ['N° Doc. externe'],
            'FA Posting Date' : ['Date compta. immo.'],
            'FA Posting Type' : ['Type compta. immo.'],
            'Depreciation Book Code' : ["Code loi d'ammortissement"],
            'Branch Code' : ['Code établissement'],
            'Main Area' : ['Zone principale'],
            'VIN' : ['VIN'],
            'Service Contract No.' : ['N° contrat atelier'],
            'Exclude Adjust. Exch. Rates' : ['Exclure ajustement taux de change'],
            'General Business Posting Group' : ['Groupe compta marché'],
            'Updated' : ['Traité'],
            'Updated Error' : ['Erreur'],
            'To Update' : ['A traiter'],
            'User ID' : ['Code utilisateur'],
            'Number Of Errors' : ["Nombre d'erreurs"],
            'Comments' : ['Commentaires'],
        }

        for line in move_lines:
            data['Journal Template Name'].append('')
            data['Line No.'].append(line.id)
            data['Account Type'].append('Client' if line.account_id.code[:3] == '411' else 'Fournisseur' if line.account_id.code[:3] == '401' else 'Général')
            data['Account No.'].append(line.account_id.code)
            data['Posting Date'].append(line.date)
            data['Document Type'].append('Facture' if line.move_id.move_type[3:] == 'invoice' else 'Avoir' if line.move_id.move_type[3:] == 'refund' else '')
            data['Document No.'].append(line.move_id.name)
            data['Description'].append(line.name)
            data['VAT%'].append(line.tax_ids.amount)
            data['Currency Code'].append('' if not line.currency_id else line.currency_id.name)
            data['Amount'].append(line.balance)
            data['Amount(LCY)'].append('')
            data['Currency Factor'].append('')
            data['Inv. Discount(LCY)'].append('')
            data['Sell-to/Buy-from No.'].append('')
            data['Posting Group'].append('')
            data['Department Code'].append('')
            data['Make Code'].append('')
            data['Salepers./Purch. Code'].append('')
            data['Source Code'].append(line.journal_id.type.upper())
            data['System-Created Entry'].append('')
            data['Due Date'].append(line.date_maturity if line.date_maturity else '')
            data['Journal Batch Name'].append('')
            data['Posting Type'].append('')
            data['Document Date'].append(line.move_id.invoice_date)
            data['External Document No.'].append('')
            data['FA Posting Date'].append('')
            data['FA Posting Type'].append('')
            data['Depreciation Book Code'].append('')
            data['Branch Code'].append('')
            data['Main Area'].append('')
            data['VIN'].append('')
            data['Service Contract No.'].append('')
            data['Exclude Adjust. Exch. Rates'].append('')
            data['General Business Posting Group'].append('C10' if line.partner_id.in_group else 'C05')
            data['Updated'].append('')
            data['Updated Error'].append('')
            data['To Update'].append('')
            data['User ID'].append('')
            data['Number Of Errors'].append('')
            data['Comments'].append('')
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
        session.storbinary('STOR Ecritures_Comptables.csv', bio)