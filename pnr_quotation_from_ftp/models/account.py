# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import UserError
from  odoo.tools.misc import formatLang

class AccountMove(models.Model):
    _inherit = 'account.move'

    other_tax = fields.Float(string="Amount Tax", compute="_compute_other_tax")
    amount_without_any_tax = fields.Float(string="Untaxed Amount", compute="_compute_other_tax")
    amount_tva = fields.Float(string="Amount TVA", compute="_compute_other_tax")

    # @api.onchange('partner_id')
    # def onchange_partner(self):
    #     raise UserError(self.tax_totals_json)

    @api.model
    def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
        res = super(AccountMove, self)._get_tax_totals(partner, tax_lines_data, amount_total, amount_untaxed, currency)

        lang_env = self.with_context(lang=partner.lang).env

        res.update({
            'amount_without_any_tax' : self.amount_without_any_tax,
            'other_tax' : self.other_tax,
            'formatted_amount_without_any_tax' : formatLang(lang_env, self.amount_without_any_tax, currency_obj=currency),
            'formatted_other_tax' : formatLang(lang_env, self.other_tax, currency_obj=currency),
        })

        return res

    @api.depends('invoice_line_ids.other_tax')
    def _compute_other_tax(self):
        for record in self:
            other_tax = 0.0
            amount_tva = record.amount_total - record.amount_untaxed
            for line in record.invoice_line_ids:
                other_tax += line.other_tax

            record.update({'other_tax' : other_tax, 'amount_without_any_tax' : record.amount_untaxed - other_tax, 'amount_tva' : amount_tva})

    @api.model
    def create(self, vals):
        if 'invoice_line_ids' in vals:
            for line in vals['invoice_line_ids']:
                if 'line_ids' in vals:
                    corresponding_line_id = [line_id for line_id in vals['line_ids'] if line_id[1] == line[1]][0]

                    sign = 1 if not 'price_unit' in corresponding_line_id[2] else int(corresponding_line_id[2]['price_unit'] / abs(corresponding_line_id[2]['price_unit']))
                    other_tax = 0 if not 'other_tax' in line[2] else line[2]['other_tax']
                    price_unit = sign * (abs(corresponding_line_id[2]['price_unit']) - other_tax)

                    if corresponding_line_id and 'other_tax' in line[2]:
                        # corresponding_line_id[2].update({'price_unit' : price_unit, 'other_tax' : other_tax})
                        corresponding_line_id[2].update({'other_tax' : other_tax})

        # Set label of 401 or 411 in journal items

        # if 'line_ids' in vals and 'global_label' in vals:
        #     raise UserError("alert from pnr_quotation_from_ftp module:\nline_ids and global_label are in vals")
        #     for line in vals['line_ids']:
        #         if line[2]:
        #             values = line[2]
        #         else:
        #             continue

        #         if values['account_id'] in (288, 303):      # 288 for 401, 303 for 411
        #             values['name'] = vals['global_label']
        #         else:
        #             values['name'] = 'account_id not in (288, 303)'

        # else:
        #     fako = ''
        #     if 'line_ids' not in vals:
        #         fako += "line_ids"
        #     if 'global_label' not in vals:
        #         fako += "global_label"
        #     raise UserError("alert from pnr_quotation_from_ftp module:\n%s is not in vals" % fako)

        invoice = super(AccountMove, self).create(vals)

        for line in invoice.invoice_line_ids:
            line.price_unit -= line.other_tax

            # if line.account_id in (288,303):
            #     line.name = invoice.global_label

        # Set label of 401 or 411 in journal items
        for line in invoice.line_ids:
            if line.account_id.id == 288:
                line.name = invoice.global_label
        #     # elif line.account_id.id == 303:
        #     #     line.name = invoice.global_label
        #     # else:
        #     line.name = 'line.account_id.id is not in (288, 303)'

        # raise UserError("alert from pnr_quotation_from_ftp module:\n account.move create method called")
        # partner_account_line = self.env['account.move.line'].search(['&', ('move_id', '=', invoice.id), ('account_id', 'in', (288, 303))])
        # partner_account_line.write({'name' : partner_account_line.move_id.global_label})

        return invoice

    # @api.depends(
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.debit',
    #     'line_ids.credit',
    #     'line_ids.currency_id',
    #     'line_ids.amount_currency',
    #     'line_ids.amount_residual',
    #     'line_ids.amount_residual_currency',
    #     'line_ids.payment_id.state',
    #     'line_ids.full_reconcile_id',
    #     'other_tax'
    # )
    # def _compute_amount(self):
    #     for move in self:

    #         if move.payment_state == 'invoicing_legacy':
    #             # invoicing_legacy state is set via SQL when setting setting field
    #             # invoicing_switch_threshold (defined in account_accountant).
    #             # The only way of going out of this state is through this setting,
    #             # so we don't recompute it here.
    #             move.payment_state = move.payment_state
    #             continue

    #         total_untaxed = 0.0
    #         total_untaxed_currency = 0.0
    #         total_tax = 0.0
    #         total_tax_currency = 0.0
    #         total_to_pay = 0.0
    #         total_residual = 0.0
    #         total_residual_currency = 0.0
    #         total = 0.0
    #         total_currency = 0.0
    #         currencies = set()

    #         for line in move.line_ids:
    #             if line.currency_id and line in move._get_lines_onchange_currency():
    #                 currencies.add(line.currency_id)

    #             if move.is_invoice(include_receipts=True):
    #                 # === Invoices ===

    #                 if not line.exclude_from_invoice_tab:
    #                     # Untaxed amount.
    #                     total_untaxed += line.balance
    #                     total_untaxed_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.tax_line_id:
    #                     # Tax amount.
    #                     total_tax += line.balance
    #                     total_tax_currency += line.amount_currency
    #                     total += line.balance
    #                     total_currency += line.amount_currency
    #                 elif line.account_id.user_type_id.type in ('receivable', 'payable'):
    #                     # Residual amount.
    #                     total_to_pay += line.balance
    #                     total_residual += line.amount_residual
    #                     total_residual_currency += line.amount_residual_currency
    #             else:
    #                 # === Miscellaneous journal entry ===
    #                 if line.debit:
    #                     total += line.balance
    #                     total_currency += line.amount_currency

    #         if move.move_type == 'entry' or move.is_outbound():
    #             sign = 1
    #         else:
    #             sign = -1
    #         move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
    #         # move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
    #         move.amount_tax = sign * ((total_tax_currency if len(currencies) == 1 else total_tax) + move.other_tax)
    #         # move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
    #         move.amount_total = sign * (total_currency if len(currencies) == 1 else total) + move.other_tax
    #         move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
    #         move.amount_untaxed_signed = -total_untaxed
    #         move.amount_tax_signed = -total_tax
    #         move.amount_total_signed = abs(total) if move.move_type == 'entry' else -total
    #         move.amount_residual_signed = total_residual

    #         currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id

    #         # Compute 'payment_state'.
    #         new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

    #         if move.is_invoice(include_receipts=True) and move.state == 'posted':

    #             if currency.is_zero(move.amount_residual):
    #                 reconciled_payments = move._get_reconciled_payments()
    #                 if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
    #                     new_pmt_state = 'paid'
    #                 else:
    #                     new_pmt_state = move._get_invoice_in_payment_state()
    #             elif currency.compare_amounts(total_to_pay, total_residual) != 0:
    #                 new_pmt_state = 'partial'

    #         if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
    #             reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
    #             reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

    #             # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
    #             reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
    #             if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
    #                 new_pmt_state = 'reversed'

    #         move.payment_state = new_pmt_state

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    other_tax = fields.Float(string="Other Taxes")

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'
        if taxes:
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(line_discount_price_unit,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal

        # res['price_subtotal'] += self.other_tax
        res['price_total'] += self.other_tax

        # In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k : currency.round(v) for k, v in res.items()}
        return res

    @api.onchange('other_tax')
    def _onchange_other_tax(self):
        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            line.update(line._get_price_total_and_subtotal())
            line.update(line._get_fields_onchange_subtotal())
