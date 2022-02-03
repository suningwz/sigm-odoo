# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 19 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Line Description Setting',
    'version' : '1.1',
    'summary': 'Line Description Setting',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Line Description SEtting
        ========================
        This module adds details on the description in the sale order lines
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'sale', 'pnr_quotation_from_ftp'],
    'data': [
        "views/sale.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
