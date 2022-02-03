# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 14 JUne 2021                                        #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Export of Contacts',
    'version' : '1.1',
    'summary': 'Export of Contacts',
    'sequence': -20,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Round Amount Total
        ==================
        This module get the contacts, writes them in a CSV file and send it to an FTP server
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
