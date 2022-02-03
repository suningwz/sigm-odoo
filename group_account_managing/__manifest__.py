# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 18 November 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Group Account Managing',
    'version' : '1.1',
    'summary': 'Group Account Managing',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Group Account Managing
        ======================
        This module manages account number used in the invoice lines according to customer is either in or out of a group
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'add_group_field_in_customer', 'add_group_fields_in_product'],
    'data': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
