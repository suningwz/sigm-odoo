# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Add In Group Field in Partner (Customer)',
    'version' : '1.1',
    'summary': 'Add In Group Fields in Partner (Customer)',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Add In Group Field in Partner
        =============================
        This module adds in_group field in res.partner model to determine if a customer is either in or out of a group
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base'],
    'data': [
        "views/partner.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
