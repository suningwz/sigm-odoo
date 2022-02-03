# -*- coding: utf-8 -*-
# ############################################################################################################
#                                   This addon was created by Muriel Rémi                                    #
#                                      Creation date: 09 December 2021                                       #
# ############################################################################################################
{
    'name' : "Travel Agency",
    'version' : '1.1',
    'summary': "Travel Agency",
    'sequence': -21,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Travel Agency
        =============
        The main objective of this module is to manage Travel
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'sale', 'global_label_fields', 'supplier_from_incadea', 'customer_type_management', 'contacts_from_incadea'],
    'data': [
        "security/ir.model.access.csv",
        "views/travel.xml",
        "views/account.xml",
        "views/product.xml",
        "views/purchase.xml",
        "report/travel_report_templates.xml",
        "report/travel_report.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
