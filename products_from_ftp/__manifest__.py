# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 31 May 2021                                         #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import Products from an FTP Server',
    'version' : '1.1',
    'summary': 'Import Products from an FTP Server',
    'sequence': -20,
    'description': """
Round Amount Total
==================
This module is created to allow odoo to import products from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account', 'travel_agency'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
