# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 23 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Global Label Fields',
    'version' : '1.1',
    'summary': 'Global Label Fields',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Global Label Fields
        ===================
        This module adds global_label field in sale.order and account.move models
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'sale'],
    'data': [
        "views/sale.xml",
        "views/account.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
