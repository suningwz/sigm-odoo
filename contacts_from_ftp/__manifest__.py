# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 19 May 2021                                         #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Import Contacts from an FTP Server',
    'version' : '1.1',
    'summary': 'Import Contacts from an FTP Server',
    'sequence': -20,
    'description': """
Round Amount Total
==================
This module is created to allow odoo to import contacts from an FTP server...
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
