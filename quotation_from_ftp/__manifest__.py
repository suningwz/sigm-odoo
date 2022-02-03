# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 31 May 2021                                         #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import Travel Quotations from an FTP Server',
    'version' : '1.1',
    'summary': 'Import Travel Quotations from an FTP Server',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
        Travel Quotation from FTP Server
        ==============================
        This module is created to allow odoo to import travel quotations from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'travel_agency'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
