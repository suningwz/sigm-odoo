# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Add In Group Fields in Product',
    'version' : '1.1',
    'summary': 'Add In Group Fields in Product',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Add In Group Fields in Product
        ==============================
        This module adds two group account fields in product.template model
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'sale'],
    'data': [
        "views/product.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
