# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 15 February 2022                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Add No G field in Res Partner',
    'version' : '1.1',
    'summary': 'Add No G field in Res Partner',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Add No G field in Res Partner
        =============================
        This module adds no_g field in res.partner model to define side account of the partner
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
