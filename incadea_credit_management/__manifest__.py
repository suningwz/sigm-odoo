# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 24 November 2021                                       #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Incadea Credit Management',
    'version' : '1.1',
    'summary': 'Incadea Credit Management',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Incadea Credit Management
        =========================
        This module allows to manage credit of Incadea's customers
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'travel_agency'],
    'data': [
        "data/cron.xml",
        "views/travel.xml",
        "views/users.xml",
        "views/partner.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
