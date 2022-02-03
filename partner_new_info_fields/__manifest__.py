# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 19 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Partner New Info Fields',
    'version' : '1.1',
    'summary': 'Partner New Info Fields',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Partner New Info Fields
        =======================
        This module adds new info fields to res.partner model
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
