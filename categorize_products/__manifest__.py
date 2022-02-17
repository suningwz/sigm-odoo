# ############################################################################################################
#                                   This module was created by Muriel Rémi                                   #
#                                       Creation date: 17 February 2022                                      #
# ############################################################################################################
# -*- coding: utf-8 -*-

{
	'name' : 'Categorize Products',
	'version' : '1.1',
	'summary' : 'Categorize Products',
	'sequence' : -20,
	'author' : 'Muriel Rémi Cyr',
	'description' : """
		Categorize Products
		===================
		This module categorizes products in ticket, fees and voucher
	""",
	'depends' : ['product'],
	'data' : ["views/product.xml"],
	'installable' : True,
	'auto_install' : False,
}