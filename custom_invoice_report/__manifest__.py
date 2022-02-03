# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 19 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Custom Invoice Report',
    'version' : '1.1',
    'summary': 'Custom Invoice Report',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Custom Invoice Report
        =====================
        This module allows to customize pdf report of invoice
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'partner_new_info_fields'],
    'data': [
        "reports/report_invoice_document.xml",
        "reports/report_invoice.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
