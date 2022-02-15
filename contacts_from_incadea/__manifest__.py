# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                      Creation date: 28 September 2021                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import Incadea Clients from an FTP Server',
    'version' : '1.1',
    'summary': 'Import Incadea Clients from an FTP Server',
    'sequence': -20,
    'author' : 'Muriel Rémi Cyr',
    'description': """
Contacts from Incadea
=====================
This module is created to allow odoo to import Incadea clients from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'group_account_managing'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
