# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 09 December 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError

from datetime import datetime as dt

from functools import partial
from odoo.tools.misc import formatLang

class TravelOrder(models.Model):
    _name = 'travel.order'
    _description = "Travel Order"

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', default=lambda self: _('New'), readonly=True, noupdate=True, copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer", state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})

    user_id = fields.Many2one(
        'res.users', string='Person', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])

    date_order = fields.Date(string="Date", default=dt.strftime(dt.now().date(), '%Y-%m-%d'), state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    date_from = fields.Date(string="From", default=dt.strftime(dt.now().date(), '%Y-%m-%d'), state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    date_to = fields.Date(string="To", state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    company_id = fields.Many2one('res.company', string="Company")

    transmitter = fields.Char(string="Transmitter", default="MERCURE", readonly=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    transmit_date = fields.Date(string="Date of Issue", state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    followed_by = fields.Many2one('hr.employee', string="Followed by", document_type={'amadeus' : [('required', True)]}, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]), state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    ref = fields.Char(string="Reference", state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    global_label = fields.Text(string="Global Label", required=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})

    state = fields.Selection([
        ('quotation', 'Quotation'), 
        ('accepted', 'Accepted'),
        ('confirmed', 'Confirmed'), 
        ('canceled', 'Canceled'),
    ], string="State", default='quotation')

    order_line = fields.One2many('travel.order.line', 'order_id', string="Travel Order Lines", auto_join=True, copy=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})

    amount_untaxed = fields.Monetary(string="Amount Untaxed", store=True, readonly=True, compute="_amount_all", tracking=5)
    amount_tax = fields.Monetary(string="Amount Tax", store=True, compute="_amount_all")
    amount_tva = fields.Monetary(string="Amount TVA", store=True, readonly=True, compute="_amount_all")
    amount_total = fields.Monetary(string="Amount Total", store=True, readonly=True, compute="_amount_all", tracking=4)
    amount_by_group = fields.Binary(string="Tax amount by group", compute="_amount_by_group", help="type : [(name, amount, base, formated amount, formated base)]")

    currency_id = fields.Many2one(related='pricelist_id.currency_id', depends=["pricelist_id"], string="Currency", readonly=True, required=True)

    company_id = fields.Many2one('res.company', string="Company")

    purchase_invoice_count = fields.Integer(string="Purchase Invoice Count", compute="_get_invoiced", readonly=True)
    sale_invoice_count = fields.Integer(string="Sale Invoice Count", compute="_get_invoiced", readonly=True)
    purchase_invoice_ids = fields.Many2many('account.move', string='Purchase Invoices', compute='_get_invoiced', readonly=True, copy=False)
    sale_invoice_ids = fields.Many2many('account.move', string='Sale Invoices', compute='_get_invoiced', readonly=True, copy=False)

    document_type = fields.Selection([('amadeus', 'Amadeus'), ('to', 'Tour Operator')], string="Document Type", required=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', True)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})



    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'quotation' : [('readonly', False)], 'confirmed' : [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )

    pricelist_id = fields.Many2one(
        'product.pricelist', string="Pricelist", check_company=True, # Unrequired company
        required=True, readonly=True, states={'quotation' : [('readonly', False)], 'confirmed' : [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="If you change the pricelist, only newly added lines will be affected."
    )

    signature = fields.Image('Signature', help='Signature received through the portal.', copy=False, attachment=True, max_width=1024, max_height=1024)

    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms or ''

    note = fields.Text('Terms and conditions', default=_default_note)

    payment_term_id = fields.Many2one(
        'account.fiscal.position', string='Payment Terms', check_company=True, # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string="Fiscal Position",
        domain="[('company_id', '=', company_id)]", check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or travels orders/invoices."
        "The default value comes from the customer."
    )

    other_infos = fields.Text(string="Other Infos")

    num_pnr = fields.Char(string="Number PNR", copy=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})
    folder_number = fields.Char(string="Folder Number", copy=True, state={'quotation' : [('readonly', False)], 'accepted' : [('readonly', False)], 'confirmed' : [('readonly', True)], 'canceled' : [('readonly', True)]})

    @api.depends('order_line.price_subtotal', 'order_line.amount_tax', 'order_line.amount_tva')
    def _amount_all(self):
        """
            Compute the total amounts of Travel Order
        """
        for order in self:
            amount_untaxed = amount_tax = amount_tva = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal - line.amount_tax
                # amount_untaxed += line.price_subtotal
                amount_tva += line.amount_tva
                amount_tax += line.amount_tax

            order.update({
                'amount_untaxed' : amount_untaxed,
                'amount_tva' : amount_tva,
                'amount_tax' : amount_tax,
                'amount_total' : amount_untaxed + amount_tva + amount_tax,
            })

    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                taxes = line.tax_ids.compute_all(price_reduce, quantity=line.quantity * line.number, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_ids:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount' : 0.0, 'base' : 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']

            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]

    def _get_invoiced(self):
        for order in self:
            # Purchase Invoices
            purchase_invoices = self.env['account.move'].search([('invoice_origin', '=', order.name), ('move_type', 'in', ('in_invoice', 'in_refund'))])
            order.purchase_invoice_ids = purchase_invoices
            order.purchase_invoice_count = len(purchase_invoices)

            # Sale Invoices
            sale_invoices = self.env['account.move'].search([('invoice_origin', '=', order.name), ('move_type', 'in', ('out_invoice', 'out_refund'))])
            order.sale_invoice_ids = sale_invoices
            order.sale_invoice_count = len(sale_invoices)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('travel.order')

        # -----------------------------------------------------
        # Create name of each travel order lines
        # -----------------------------------------------------
        # raise UserError(str(vals))
        if 'order_line' in vals:
            for line in vals['order_line']:
                values = line[2]
                name_elements = [
                    '' if not 'journey' in values else values['journey'], 
                    '' if not 'ticket_number' in values else values['ticket_number'], 
                    '' if not 'passenger' in values else values['passenger'], 
                    '' if not 'custom_descri' in values else values['custom_descri']
                ]
                name_elements = [item for item in name_elements if item]
                if any(name_elements):
                    values.update({'name' : ' - '.join(name_elements)})
                else:
                    values.update({'name' : self.env['product.product'].browse(values['product_id']).name})
        # -----------------------------------------------------

        return super(TravelOrder, self).create(vals)

    def write(self, vals):
        # -----------------------------------------------------
        # Create name of each travel order lines
        # -----------------------------------------------------
        if 'order_line' in vals:
            for line in vals['order_line']:
                values = line[2]
                if not values:
                    continue

                if 'product_id' in values:
                    if line[0] == 0:        # New line
                        tol = self.env['travel.order.line']
                    else:
                        tol = self.env['travel.order.line'].browse(line[1])

                    name_elements = [
                        ('' if not 'journey' in values else values['journey']) or tol.journey, 
                        ('' if not 'ticket_number' in values else values['ticket_number']) or tol.ticket_number, 
                        ('' if not 'passenger' in values else values['passenger']) or tol.passenger, 
                        ('' if not 'custom_descri' in values else values['custom_descri']) or tol.custom_descri, 
                    ]

                    name_elements = [item for item in name_elements if item]
                    if any(name_elements):
                        values.update({'name' : ' - '.join(name_elements)})
                    else:
                        values.update({'name' : self.env['product.product'].browse(values['product_id']).name})
        # -----------------------------------------------------
        return super(TravelOrder, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state in ('accepted', 'confirmed'):
                raise UserError(_("You cannot delete document that has been %s!") % (_("accepted") if record.state == 'accepted' else _("confirmed")))
            else:
                super(TravelOrder, record).unlink()

    @api.onchange('partner_id')
    def onchange_partner(self):
        """
            Update the following fields when the partner is changed:
            - Pricelist
            - Payment terms
            - Invoice address
            - Delivery address
        """
        if not self.partner_id:
            self.update({
                'partner_shipping_id' : False,
                'fiscal_position_id' : False
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id

        values = {
            'pricelist_id' : self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id' : self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_shipping_id' : addr['delivery'],
        }
        user_id = partner_user.id

        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.uid
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.user_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        self.update(values)

    def action_accept(self):
        # ------------------------------------------------------
        # Create purchase order
        # ------------------------------------------------------
        purchase_orders = {}
        for line in self.order_line:
            if line.supplier:
                if not line.supplier in purchase_orders:
                    purchase_orders[line.supplier] = {
                        'partner_id' : line.supplier.id,
                        'currency_id' : line.currency_id.id,
                        'date_order' : dt.strftime(dt.now().date(), '%Y-%m-%d'),
                        'travel_order_id' : self.id,
                        'order_line' : []
                    }

                purchase_orders[line.supplier]['order_line'].append((0,0,{
                    'product_id' : line.product_id.id,
                    'name' : line.name,
                    'product_qty' : line.quantity * line.number,
                    'price_unit' : line.price_unit,
                    'other_tax' : line.amount_tax,
                }))

        for partner in purchase_orders:
            purchase_order = self.env['purchase.order'].create(purchase_orders[partner])
            purchase_order.button_confirm()
        # ------------------------------------------------------
        old_state = dict(self._fields['state'].selection).get(self.state)
        self.update({'state' : 'accepted'})
        new_state = dict(self._fields['state'].selection).get(self.state)

        message_body = _("State : %s → %s") % (old_state, new_state)

        self.message_post(body=message_body)

    def action_confirm(self):
        if not self.env.user.can_confirm_no_quotation:
            # ------------------------------------------------------
            # Create Customer Invoices and confirm them
            # ------------------------------------------------------
            invoice_values = {
                'partner_id' : self.partner_id.id,
                'invoice_date' : dt.strftime(dt.now().date(), '%Y-%m-%d'),
                'global_label' : self.global_label,
                'move_type' : 'out_invoice',
                'journal_id' : 1,
                # 'company_id' : self.company_id.id,
                'invoice_origin' : self.name,
                'currency_id' : self.currency_id.id,
                'invoice_line_ids' : [],
            }

            if self.document_type == 'to' :
                for line in self.order_line:
                    invoice_line = (0,0,{
                        'product_id' : line.product_id.id,
                        'name' : line.name,
                        'quantity' : line.quantity * line.number,
                        'price_unit' : line.price_unit,
                        # 'tax_ids' : line.tax_ids,
                        # 'other_tax' : line.amount_tax,
                    })

                    invoice_values['invoice_line_ids'].append(invoice_line)

                # -----------------------------#
                # Append line commission
                # -----------------------------#

                # Search for product commission
                commission_product = self.env['product.product'].search([('name', '=', "COMMISSION")])

                if not commission_product :
                    commission_product = self.env['product.product'].create({'name':'COMMISSION'})

                # Compute amount commission
                
                amount_commission_total = self.amount_total - sum([line.price_unit for line in self.order_line ]) 
                amount_commission_unit = amount_commission_total - self.amount_tva
                commission_line = (0,0,{
                        'product_id' : commission_product.id,
                        'name' : commission_product.name,
                        'quantity' : 1,
                        'price_unit' : amount_commission_unit,
                        'tax_ids' : self.order_line[0].tax_ids,
                        # 'other_tax' : line.amount_tax,
                    })
                invoice_values['invoice_line_ids'].append(commission_line)

            else :
                for line in self.order_line:
                    invoice_line = (0,0,{
                        'product_id' : line.product_id.id,
                        'name' : line.name,
                        'quantity' : line.quantity * line.number,
                        'price_unit' : line.price_unit,
                        'tax_ids' : line.tax_ids,
                        'other_tax' : line.amount_tax,
                    })

                    invoice_values['invoice_line_ids'].append(invoice_line)

            customer_invoice = self.env['account.move'].create(invoice_values)
            customer_invoice.action_post()
            # ------------------------------------------------------

            # ------------------------------------------------------
            # Create invoice for the suppliers and confirm them
            # ------------------------------------------------------
            # supplier_invoices = {}
            # for line in self.order_line:
            #     if line.supplier:
            #         if not line.supplier in supplier_invoices:
            #             supplier_invoices[line.supplier] = {
            #                 'partner_id' : line.supplier.id,
            #                 'ref' : _("Travel Invoice : %s") % self.name,
            #                 'move_type' : 'in_invoice',
            #                 'invoice_date' : dt.strftime(dt.now().date(), '%Y-%m-%d'),
            #                 'currency_id' : self.currency_id,
            #                 'invoice_origin' : self.name,
            #                 'invoice_line_ids' : []
            #             }

            #         supplier_invoices[line.supplier]['invoice_line_ids'].append((0,0,{
            #             'product_id' : line.product_id.id,
            #             'name' : line.name,
            #             'quantity' : line.quantity,
            #             'price_unit' : line.price_unit,
            #             'tax_ids' : line.tax_ids,
            #             'other_tax' : line.amount_tax,
            #         }))

            # for partner in supplier_invoices:
            #     purchase_invoice = self.env['account.move'].create(supplier_invoices[partner])
            #     purchase_invoice.action_post()
            # ------------------------------------------------------

            # ------------------------------------------------------
            # Confirm invoice of corresponding purchase order
            # ------------------------------------------------------
            related_PO = self.env['purchase.order'].search([('travel_order_id', '=', self.id), ('state', '=', 'purchase')])
            for po in related_PO:
                supplier_invoice = po.action_create_invoice()

                # raise UserError(str(supplier_invoice))

                supplier_invoice = self.env['account.move'].browse(supplier_invoice['res_id'])

                supplier_invoice.update({'ref' : _("Travel Invoice : %s") % self.name, 'invoice_date' : dt.strftime(dt.now().date(), '%Y-%m-%d'), 'global_label' : self.global_label, 'invoice_origin' : self.name})

                supplier_invoice.action_post()

                # raise UserError(str(supplier_invoices))

                # for invoice in supplier_invoices:
                #     invoice.update({'ref' : _("Travel Invoice : %s") % self.name, 'invoice_date' : dt.strftime(dt.now().date(), '%Y-%m-%d'), 'global_label' : self.global_label, 'invoice_origin' : self.name})
            # ------------------------------------------------------
            old_state = dict(self._fields['state'].selection).get(self.state)
            self.update({'state' : 'confirmed'})
            new_state = dict(self._fields['state'].selection).get(self.state)

            message_body = _("State : %s → %s") % (old_state, new_state)

            self.message_post(body=message_body)
        else:
            raise UserError(_("You don't have the right to confirm a quotation!"))

    def action_cancel(self):
        related_PO = self.env['purchase.order'].search([('travel_order_id', '=', self.id)])
        related_PO.button_cancel()
        related_PO.unlink()

        old_state = dict(self._fields['state'].selection).get(self.state)
        self.update({'state' : 'canceled'})
        new_state = dict(self._fields['state'].selection).get(self.state)

        message_body = _("State : %s → %s") % (old_state, new_state)

        self.message_post(body=message_body)

    def action_make_quotation(self):
        old_state = dict(self._fields['state'].selection).get(self.state)
        self.update({'state' : 'quotation'})
        new_state = dict(self._fields['state'].selection).get(self.state)

        message_body = _("State : %s → %s") % (old_state, new_state)

        self.message_post(body=message_body)

    def action_view_purchase_invoice(self):
        purchase_invoices = self.mapped('purchase_invoice_ids')
        action = self.env.ref('account.action_move_in_invoice_type').read()[0]

        if len(purchase_invoices) > 1:
            action['domain'] = [('id', 'in', purchase_invoices.ids)]
        elif len(purchase_invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view

            action['res_id'] = purchase_invoices.id
        else:
            action = {'type' : 'ir.actions.act_window_close'}

        context = {
            'default_type' : 'in_invoice',
        }

        if len(self) == 1:
            context.update({
                'default_partner_id' : self.partner_id.id,
                # 'default_partner_shipping_id' : self.partner_shipping_id.id,
                # 'default_invoice_payment_term_id' : self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
                'default_invoice_origin' : self.mapped('name'),
                # 'default_user_id' : self.user_id.id,
            })

        action['context'] = context

        return action

    def action_view_sale_invoice(self):
        sale_invoices = self.mapped('sale_invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]

        if len(sale_invoices) > 1:
            action['domain'] = [('id', 'in', sale_invoices.ids)]
        elif len(sale_invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view

            action['res_id'] = sale_invoices.id
        else:
            action = {'type' : 'ir.actions.act_window_close'}

        context = {
            'default_type' : 'out_invoice',
        }

        if len(self) == 1:
            context.update({
                'default_partner_id' : self.partner_id.id,
                # 'default_partner_shipping_id' : self.partner_shipping_id.id,
                # 'default_invoice_payment_term_id' : self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
                'default_invoice_origin' : self.mapped('name'),
                # 'default_user_id' : self.user_id.id,
            })

        action['context'] = context

        return action

    def print_quotation_order(self):
        return self.env.ref('travel_agency.action_report_travelorder').report_action(self)

    def print_proforma(self):
        return self.env.ref('travel_agency.action_report_travelorder_proforma').report_action(self)

class TravelOrderLine(models.Model):
    _name = 'travel.order.line'
    _description = 'Travel Order Line'

    product_id = fields.Many2one('product.product', string="Product", domain="[('active_product', '=', True)]")
    name = fields.Char(string="Description")
    # supplier = fields.Many2one('res.partner', string="Supplier", domain="[('supplier_rank', '=', 1)]")
    passenger = fields.Char(string="Passenger")
    ticket_number = fields.Char(string="Ticket Number")
    journey = fields.Char(string="Journey")
    custom_descri = fields.Char(string="Custom Description")
    number = fields.Integer(string="Number", default=1)
    quantity = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Float(string="Price Unit")
    percent_commission = fields.Float(string="Commission (%)")
    amount_commission = fields.Float(string="Commission (Amount)", compute='compute_amount_commission')
    discount = fields.Float(string="Discount (%)", digits="Discount", default=0.0)
    tax_ids = fields.Many2many('account.tax', string="VAT")
    amount_tax = fields.Float(string="Other Taxes")
    amount_tva = fields.Float(string="Amount TVA", compute="_compute_amount")
    price_subtotal = fields.Float(string="Subtotal", compute="_compute_amount")
    price_total = fields.Float(string="Total", compute="_compute_amount")
    price_tax = fields.Float(string="Total Tax", compute="_compute_amount", readonly=True, store=True)

    order_id = fields.Many2one('travel.order', string="Order Reference", ondelete="cascade", readonly=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")
    ], default=False, help="Technical field for UX purpose.")

    currency_id = fields.Many2one(related='order_id.currency_id', depends=['order_id.currency_id'], store=True, string='Currency', readonly=True)

    day = fields.Many2one('res.day', string="Day")

    supplier = fields.Many2one('res.partner', string="Supplier", domain="[('id_supplier_incadea', '!=', False), ('active_supplier', '=', True)]")
    # --------------------------------------------------------
    # Compute amount commission value
    # --------------------------------------------------------
    @api.depends('price_unit','percent_commission')
    def compute_amount_commission(self):
        # if self.percent_commission < 0 :
        #     raise UserError('Invalid percent commission value.')
        # else :
        for line in self :
            line.amount_commission = (line.price_unit * line.percent_commission) / 100.0

    # --------------------------------------------------------
    # Name Auto setting
    # --------------------------------------------------------
    @api.onchange('product_id')
    def onchange_product(self):
        name_elements = [self.journey, self.ticket_number, self.passenger, self.custom_descri]

        name_elements = [item for item in name_elements if item]
        if any(name_elements):
            self.update({'name' : ' - '.join(name_elements)})
        else:
            self.update({'name' : self.product_id.name})

        # Set tax_ids field if needed
        self.update({'tax_ids' : self.product_id.taxes_id})

        # Filter supplier
        active_suppliers = [seller.name for seller in self.product_id.seller_ids]
        suppliers = self.env['res.partner'].search([('id_supplier_incadea', '!=', False)])

        for supplier in suppliers:
            if self.product_id:
                supplier.write({'active_supplier' : supplier in active_suppliers})
            else:
                supplier.write({'active_supplier' : True})

    @api.onchange('supplier')
    def onchange_supplier(self):
        # Filter product
        seller = self.env['product.supplierinfo'].search([('name', '=', self.supplier.id)])

        products = self.env['product.product'].search([])

        for product in products:
            if self.supplier:
                product.write({'active_product' : seller in product.seller_ids})
            else:
                product.write({'active_product' : True})

    @api.onchange('passenger')
    def onchange_passenger(self):
        name = []
        if self.journey:
            name.append(self.journey)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.passenger:
            name.append(self.passenger)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = " - ".join(name)

    @api.onchange('ticket_number')
    def onchange_ticket_number(self):
        name = []
        if self.journey:
            name.append(self.journey)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.passenger:
            name.append(self.passenger)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = " - ".join(name)

    @api.onchange('journey')
    def onchange_journey(self):
        name = []
        if self.journey:
            name.append(self.journey)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.passenger:
            name.append(self.passenger)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = " - ".join(name)

    

    @api.onchange('custom_descri')
    def onchange_custom_descri(self):
        name = []
        if self.journey:
            name.append(self.journey)
        if self.ticket_number:
            name.append(self.ticket_number)
        if self.passenger:
            name.append(self.passenger)
        if self.custom_descri:
            name.append(self.custom_descri)
        self.name = " - ".join(name)
    # --------------------------------------------------------

    @api.depends('quantity', 'number', 'discount', 'price_unit', 'tax_ids', 'amount_tax', 'amount_commission')
    def _compute_amount(self):
        """
            Compute the amounts of the Travel Order Line
        """
        for line in self:
            price = line.amount_commission if line.mapped('order_id').document_type == 'to' else line.price_unit # * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(price, line.order_id.currency_id, line.quantity * line.number, product=line.product_id, partner=line.order_id.partner_shipping_id)

            line.update({
                'amount_tva' : sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_tax' : sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])) + line.amount_tax,
                'price_total' : taxes['total_included'] + line.amount_tax + (line.quantity *line.number * line.price_unit) if line.mapped('order_id').document_type == 'to' else taxes['total_included'] + line.amount_tax ,
                'price_subtotal' : taxes['total_excluded'] + line.amount_tax + (line.quantity * line.price_unit) if line.mapped('order_id').document_type == 'to' else taxes['total_excluded'] + line.amount_tax ,
                # 'price_subtotal' : taxes['total_excluded'] + (line.quantity * line.number * line.price_unit) if line.mapped('order_id').document_type == 'to' else taxes['total_excluded'] ,
            })