# -*- coding: utf-8 -*-
# ############################################################################################################
#                                   This addon was created by Muriel Rémi                                    #
#                                      Creation date: 17 February 2022                                       #
# ############################################################################################################
{
    'name' : "Hide some buttons in Purchase Order document",
    'version' : '1.1',
    'summary': "Hide Purchase Order Buttons",
    'sequence': -21,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Hide Purchase Order Buttons
        =========================
        This module hide some buttons like 'create invoice', 'send order by mail', 'cancel', 'block' from purchase order document
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['purchase'],
    'data': [
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
