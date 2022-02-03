# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                         Creation date: 11 JUne 2021                                        #
# ############################################################################################################
# -*- coding: utf-8 -*-
{
    'name' : 'Export of Account Move Line',
    'version' : '1.1',
    'summary': 'Export of Account Move Line',
    'sequence': -20,
    'author' : "Muriel Rémi Cyr",
    'description': """
        Export of Account Move Line
        ===========================
        This module get the lines in the Account Move Line Model, writes them in a CSV file and send it to an FTP server
    """,
    'category': '',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base', 'account'],
    'data': [
        'data/cron.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
