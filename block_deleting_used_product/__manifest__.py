# -*- coding: utf-8 -*-
# ############################################################################################################
#                                   This addon was created by Muriel Rémi                                    #
#                                      Creation date: 03 February 2022                                       #
# ############################################################################################################
{
    'name' : "Block deleting used product",
    'version' : '1.1',
    'summary': "Block deleting used product",
    'sequence': -21,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Block deleting used product
        ===========================
        This module shows an alert when a product used in a travel order is getting to be deleted
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'travel_agency'],
    'data': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
