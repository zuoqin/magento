# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product Sequence',
    'version': '0.1',
    "author": "Zikzakmedia SL",
    "website": "http://www.zikzakmedia.com",
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "description": """
This module allows to associate a sequence to the product reference.
The reference (default code) is unique (SQL constraint) and required.

Note: This module is incompatible with nan_product_sequence.
    """,
    'depends': [
        'product_unique_code',
    ],
    "data": [
        'product_sequence.xml',
    ],
    'installable': True,
    'active': False,
}