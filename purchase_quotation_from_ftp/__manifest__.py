# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 30 September 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import Purchase Quotations from an FTP Server',
    'version' : '1.1',
    'summary': 'Import Purchase Quotations from an FTP Server',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
Purchase Quotation from FTP Server
==================================
This module is created to allow odoo to import purchase quotations from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'purchase'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
