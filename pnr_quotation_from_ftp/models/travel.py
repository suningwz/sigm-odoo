# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 07 Septembre 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError
import json
import os
import ftplib
from cryptography.fernet import Fernet
from io import BytesIO
import pandas as pd
from datetime import datetime as dt

from  odoo.tools.misc import formatLang


class TravelOrder(models.Model):

    _inherit = "travel.order"

    pnr_number = fields.Char(String="Quotation PNR Number")

    def import_qpnr_from_ftp(self):
        
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
        folder_source = _CONFIG_['csvfiles']['source']

        
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

            # filename = 'ExportedPnr.csv'
            filename = 'pnrExport.csv'

            byte = BytesIO()
            session.retrbinary('RETR ' + filename, byte.write)
            byte.seek(0)

            quotations_data = pd.read_csv(byte, encoding='latin1')
            quotations_data = quotations_data.fillna("")

            byte.close()
            session.quit()

        # ------------------------------------------------------------------------------------
        #                            Import Quotations from csv file                         #
        # ------------------------------------------------------------------------------------
        # Convert pandas dataframe into json like data
        quotations = {}
        for index, row in quotations_data.iterrows():
            RecordLocator = ' '.join(row['RecordLocator'].split())
            raise UserError("%s : %s" % (RecordLocator, type(RecordLocator)))
            if not RecordLocator in quotations:
                Doit = ' '.join(row['Doit'].split())
                Adresse = ' '.join(row['Adresse'].split())
                followed_by = ' '.join(row['Suivi par'].split())

                if Doit:
                    client = self.env['res.partner'].search([('name', '=', Doit)])
                else:
                    client = self.env['res.partner'].search([('name', '=', 'Client Temporaire')])
                if not len(client.ids):
                    client = self.env['res.partner'].create({'name' : Doit, 'street' : Adresse})

                follower = self.env['hr.employee'].search([('name', '=', followed_by)])

                addr = client.address_get(['delivery', 'invoice'])

                currency = self.env['res.currency'].search([('name', '=', ' '.join(row['FareCurrency'].split()))])

                quotations[RecordLocator] = {
                    'pnr_number' : RecordLocator,
                    'num_pnr' : RecordLocator,
                    'record_locator' : RecordLocator,
                    # 'date_order' : dt.strptime(row['Date'], '%m/%d/%Y') if row['Date'] != '' else None,
                    # 'creation_date' : dt.strptime(row['CreationDate'], '%m/%d/%Y') if row['CreationDate'] != '' else None,
                    'transmitter' : ' '.join(row['Emission'].split()),
                    # 'transmit_date' : dt.strptime(row["Date d'émission"],'%m/%d/%Y') if row["Date d'émission"] != '' else dt.today(),
                    'followed_by' : follower.id,
                    # 'ref' : ' '.join(row['Réf. Cde'].split()),
                    # 'due_date' : dt.strptime(row['Echéance'], '%m/%d/%Y') if row['Echéance'] != '' else None,
                    'partner_id' : client.id,
                    'agent_sign_booking' : ' '.join(row['AgentSignBooking'].split()),
                    # 'change_date' : dt.strptime(row['ChangeDate'], '%m/%d/%Y') if row['ChangeDate'] != '' else None,
                    # 'last_transaction_date' : dt.strptime(row['LastTransactionDate'], '%m/%d/%Y') if row['LastTransactionDate'] != '' else None,
                    'flight_class' : ' '.join(row['FlightClass'].split()),
                    'orig_city' : ' '.join(row['OrigCity'].split()),
                    'dest_city' : ' '.join(row['DestCity'].split()),
                    'service_carrier' : ' '.join(row['ServiceCarrier'].split()),
                    'flight_num' : ' '.join(str(row['FlightNo']).split()),
                    'bkg_class' : ' '.join(row['BkgClass'].split()),
                    'airport_code_origin' : ' '.join(row['AirportCodeOrigin'].split()),
                    'ama_name_origin' : ' '.join(row['AmaNameOrigin'].split()),
                    'country_origin' : self.env['res.country'].search([('code', '=', ' '.join(row['CountryOrigin'].split()))]).id, # else None,
                    'airport_code_destination' : ' '.join(row['AirportCodeDestination'].split()),
                    'ama_name_destination' : ' '.join(row['AmaNameDestination'].split()),
                    'country_destination' : self.env['res.country'].search([('code', '=', ' '.join(row['CountryDestination'].split()))]).id, # else None,
                    # 'terminal_arrival' : row['TerminalArrival'],
                    'ac_rec_loc' : ' '.join(row['AcRecLoc'].split()),
                    # 'action_date' : dt.strptime(row['ActionDate'], '%m/%d/%Y %H:%M') if row['ActionDate'] != '' else None,

                    # 'date_order' : dt.today(),# dt.strptime(row["Echéance"], '%Y-%m-%d') if row["Echéance"] != '' else ,
                    'document_type' : 'amadeus',
                    'global_label' : 'Global Label',
                    'pricelist_id' : client.property_product_pricelist and client.property_product_pricelist.id or False,
                    'partner_shipping_id' : addr['delivery'],
                    'lines' : [],
                }

            product_name = ' '.join(row['Type'].split())
            product = self.env['product.product'].search([('name', '=', product_name)])
            # if not len(product.ids):
            #     product = self.env['product.product'].create({'name' : product_name, 'used_for' : 'amadeus', 'type' : 'service'})

            title = ' '.join(row['Title'].split())
            lastname = ' '.join(row['LastName'].split())
            firtsname = ' '.join(row['FirstName'].split())

            # Trajet1 = ' '.join(str(row['Trajet1']).split())
            # Billet = ' '.join(str(row['Billet']).split())
            # Designation = ' '.join(row['Désignation'].split())
            # Usager = ' '.join(row['Usager'].split())
            # Usager = ' '.join((Designation, Usager)) if Usager != 'Inconnue' else ''
            # name_elements = [item for item in (Trajet1, Billet, Usager) if item]

            quotations[row[RecordLocator]]['lines'].append({
                'num_pnr' : row['# Id'],
                'product_id' : product.id,
                'title' : title.lower(),
                'passenger_firstname' : firstname,
                'passenger_lastname' : lastname,
                'status' : ' '.join(row['Status'].split()),
                'ticket_number' : ' '.join(row['No'].split()),
                'start_point' : ' '.join(row['OrigCity'].split()),
                'end_point' : ' '.join(row['DestCity'].split()),
                # 'departure_datetime' : dt.strptime(row['DepartureDate'], '%m/%d/%Y %H:%M') if row['DepartureDate'] != '' else None,
                # 'arrival_datetime' : dt.strptime(row['ArrivalDate'], '%m/%d/%Y %H:%M') if row['ArrivalDate'] != '' else None,
                'baggage_allow' : ' '.join(row['BaggageAllow'].split()),
                'terminal_check_in' : ' '.join(row['TerminalCheckIn'].split()),
                'terminal_arrival' : ' '.join(row['TerminalArrival'].split()),

                # 'journey' : Trajet1,
                # 'passenger' : Usager,
                # 'name' : ' - '.join(name_elements),
                # 'price_unit' : row['Transport'],
                # 'product_uom_qty' : row['quantity'],
                # 'amount_tax' : row['Taxe'],
                # 'price_total' : row['Total'],
                # 'currency_id' : currency
            })

        # Import of quotations with their lines
        for number in quotations:
            quotation = self.env['travel.order'].search([('pnr_number', '=', number)])

            # If quotation exists, check for changes
            if len(quotation.ids):
                change = False
                for key in quotations[number]:
                    if key != 'lines':
                        if quotation[key] != quotations[number][key]:
                            change = True

                if change:
                    quotation.write({key : quotations[number][key] for key in quotations[number] if key != 'lines'})
            else:
                new_quotation = {key : quotations[number][key] for key in quotations[number] if key != 'lines'}

                quotation = self.env['travel.order'].create(new_quotation)

            # Order Line update or creation
            for line in quotations[number]['lines']:
                travel_order_line = self.env['travel.order.line'].search([('num_pnr', '=', line['num_pnr'])])

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

class TravelOrderLine(models.Model):
    _inherit = 'travel.order.line'

    num_pnr = fields.Char(string="Travel Order Line Number PNR")
    designation = fields.Char(string="Designation")

    # @api.depends('amount_tax')
    # def _compute_amount(self):
    #     super(SaleOrderLine, self)._compute_amount()

    #     for line in self:
    #         line.update({
    #             # 'price_tax' : line['price_tax'] + line.amount_tax,
    #             # 'price_total' : line['price_total'] + line.amount_tax,
    #             'price_subtotal' : line['price_subtotal'] + line.amount_tax,
    #         })

    # def _prepare_invoice_line(self, **optional_values):
    #     res = super(SaleOrderLine, self)._prepare_invoice_line()
    #     res.update({'other_tax' : self.amount_tax})
    #     return res
    
# class AccountMove(models.Model):
#     _inherit = "account.move"

#     @api.model
#     def create(self, vals):
#         # raise UserError(str(vals))
#         if 'invoice_line_ids' in vals:
#             for line in vals['invoice_line_ids']:
#                 if 'line_ids' in vals:
#                     corresponding_line_id = [line_id for line_id in vals['line_ids'] if line_id[1] == line[1]][0]

#                     sign = 1 if not 'price_unit' in corresponding_line_id[2] else int(corresponding_line_id[2]['price_unit'] / abs(corresponding_line_id[2]['price_unit']))
#                     other_tax = 0 if not 'other_tax' in line[2] else line[2]['other_tax']
#                     price_unit = sign * (abs(corresponding_line_id[2]['price_unit']) - other_tax)

#                     if corresponding_line_id and 'other_tax' in line[2]:
#                         # corresponding_line_id[2].update({'price_unit' : price_unit, 'other_tax' : other_tax})
#                         corresponding_line_id[2].update({'other_tax' : other_tax})

#         invoice = super(AccountMove, self).create(vals)

#         for line in invoice.invoice_line_ids:
#             line.price_unit -= line.other_tax

#         return invoice
