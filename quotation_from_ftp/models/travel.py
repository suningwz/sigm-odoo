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

class TravelOrder(models.Model):

    _inherit = "travel.order"

    def import_from_ftp(self):
        
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
        #                                Connection to the ftp                               #
        # ------------------------------------------------------------------------------------
        state, session = False, None

        try:
            session = ftplib.FTP(ftp_host, ftp_user, ftp_pwd)
            state = True
        except Exception as e:
            print("Error : Impossible to connect to the FTP server\n{}".format(e))

        # ------------------------------------------------------------------------------------
        #                          Retrieving files from the FTP server                      #
        # ------------------------------------------------------------------------------------
        if state:
            session.cwd(folder_source)

            # filename = 'quotations.json'
            filename = 'testharo_quotations.json'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)
            quotations_data = json.load(byte)

        # ------------------------------------------------------------------------------------
        #                            Import Quotations from csv file                         #
        # ------------------------------------------------------------------------------------
        # Convert pandas dataframe into json like data
        quotations = {}
        for row in quotations_data:
            if not row['quotation_id'] in quotations:
                client_id = 'c' + str(row['customer_id'])
                # client = self.env['res.partner'].search([('id_hfsql', '=', client_id)])
                client = self.env['res.partner'].search([('name', '=', 'Client Test')])
                #Currency
                currency = self.env['res.currency'].search([('name', '=', row['currency'])])
                price_list = self.env['product.pricelist'].search([('currency_id', '=', currency.id)])

                # If the client in the current line is not in odoo yet,
                # This loop will be skiped and quotation won't be imported
                if not len(client.ids):
                    # continue
                    #client = self.env['res.partner'].create({'name' : row['client_name'], 'id_hfsql' : client_id})
                    client = self.env['res.partner'].create({'name' : 'Client Test'})

                # unique_product = self.env['product.product'].search([('name', '=', 'TOURS')])

                # if not unique_product.id:
                #     unique_product = self.env['product.product'].create({'name' : 'TOURS'})

                addr = client.address_get(['delivery', 'invoice'])

                quotations[row['quotation_id']] = {
                    'id_hfsql' : row['quotation_id'],
                    'document_type' : 'to',
                    'partner_id' : client.id,
                    # 'reference' : row['reference'],
                    'global_label' : row['global_label'],
                    'ref' : row['reference'],
                    # 'date_order' : row['date'],
                    'currency_id': currency.id,
                    'pricelist_id' : price_list.id,
                    'date_from' : row['from'],
                    'date_to' : row['to'],
                    'pricelist_id' : client.property_product_pricelist and client.property_product_pricelist.id or False,
                    'payment_term_id' : client.property_payment_term_id and client.property_payment_term_id.id or False,
                    'partner_shipping_id' : addr['delivery'],
                    # 'lines' : [{
                    #     'id_hfsql' : row['quotation_id'],
                    #     'product_id' : unique_product.id,
                    #     'name' : row['reference'],
                    #     # 'name' : 'test for naming sale order line',
                    #     'price_unit' : 0,
                    #     'product_uom_qty' : 1,
                    #     'currency_id' : currency.id
                    # }],
                    'lines' : [],
                }


            product = self.env['product.product'].search([('id_hfsql', '=', int(row['product_id']))])
            if row['supplier_id']:
                supplier = self.env['res.partner'].search([('id_supplier_incadea', '=', row['supplier_id'])])
            else:
                supplier = None
            day = self.env['res.day'].search([('name', '=', 'Jour ' + str(row['day']))])

            quotations[row['quotation_id']]['lines'].append({
                'id_hfsql' : row['quotation_line_id'],
                'product_id' : product.id,
                'name' : product.name if product.name else '',
                # 'display_type' : 'line_section'
                'supplier' : supplier.id if supplier else None,
                'day' : day.id if day else None,
                'price_unit' : row['price_unit'],
                'commission' : row['commission'],
                'discount' : row['discount'],
                'quantity' : row['quantity'],
                'amount_tax' : row['other_tax'],
            })

            # firstline = quotations[row['quotation_id']]['lines'][0]
            # firstline.update({
            #     'price_unit' : firstline['price_unit'] + row['price'] * row['quantity']
            # })

        # Import of quotations with their lines
        for id in quotations:
            quotation = self.env['travel.order'].search([('id_hfsql', '=', id)])

            # If quotation exists, check for changes
            if len(quotation.ids):
                change = False
                for key in quotations[id]:
                    if key != 'lines':
                        if quotation[key] != quotations[id][key]:
                            change = True

                if change:
                    quotation.write({key : quotations[id][key] for key in quotations[id] if key != 'lines'})
            else:
                quotation = self.env['travel.order'].create({key : quotations[id][key] for key in quotations[id] if key != 'lines'})

            # Order Line update or creation
            for line in quotations[id]['lines']:
                # If the product in the current line is not in odoo yet,
                # The line of the quotation won't be imported
                if 'product_id' in line and not line['product_id']:
                    continue

                travel_order_line = self.env['travel.order.line'].search([('id_hfsql', '=', int(line['id_hfsql']))])

                # If line exists, check for changes
                if len(travel_order_line.ids):
                    change = False
                    for key in line:
                        if line[key] != travel_order_line[key]:
                            change = True

                    if change:
                        travel_order_line.write(line)
                else:
                    line.update({'order_id' : quotation.id})
                    travel_order_line = self.env['travel.order.line'].create(line)

    id_hfsql = fields.Integer(String="Quotation ID HFSQL")


class TravelOrderLine(models.Model):
    _inherit = 'travel.order.line'

    id_hfsql = fields.Integer(string="Travel Order Line ID HFSQL")