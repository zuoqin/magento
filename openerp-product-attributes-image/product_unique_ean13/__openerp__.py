# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#    Copyright (C) 2013-TODAY Akretion <http://www.akretion.com>.
#     @author Chafique DELLI <chafique.delli@akretion.com>
#     @author David BEAL<david.beal@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Product Unique Ean13',
    'version': '0.9',
    "author": "Akretion",
    "website": "http://www.akretion.com",
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "description": """
This module allows to verify that the Ean13 field is unique (SQL constraint).
    """,
    'depends': [
        'product',
    ],
    "data": [
    ],
    'installable': True,
    'active': False,
}
