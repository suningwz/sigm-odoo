# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 07 Septembre 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import PNR Quotations from an FTP Server',
    'version' : '1.1',
    'summary': 'Import PNR Quotations from an FTP Server',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Import PNR Quotations from an FTP Server
        ========================================
        This module is created to allow odoo to import PNR quotations from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'travel_agency'],
    'data': [
        'data/cron.xml',
        'views/account.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
