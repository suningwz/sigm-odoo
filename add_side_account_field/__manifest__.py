# -*- coding: utf-8 -*-
# ############################################################################################################
#                                   This addon was created by Muriel Rémi                                    #
#                                      Creation date: 02 February 2022                                       #
# ############################################################################################################
{
    'name' : "Add Side Account Field",
    'version' : '1.1',
    'summary': "Add Side Account Field",
    'sequence': -21,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Add Side Account Field
        ======================
        This module has as main objective to add side account field in the account.move.line model
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'sale', 'global_label_fields', 'supplier_from_incadea', 'customer_type_management'],
    'data': [
        "views/account.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
