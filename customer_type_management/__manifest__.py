# -*- coding: utf-8 -*-
# ############################################################################################################
#                                   This addon was created by Muriel Rémi                                    #
#                                      Creation date: 29 December 2021                                       #
# ############################################################################################################
{
    'name' : "Customer Type Management",
    'version' : '1.1',
    'summary': "Customer Type Management",
    'sequence': -21,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Customer Type Management
        ========================
        This module is created to manage type of customer
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
