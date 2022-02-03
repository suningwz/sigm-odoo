# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Sync Sale Purchase Invoice',
    'version' : '1.1',
    'summary': 'Synchronize Sale and Purchase Invoice',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Sync Sale Purchase Invoice
        ==========================
        This modules allow to synchronize sale and purchase invoice
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'sale', 'account'],
    'data': [
        "views/sale.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
