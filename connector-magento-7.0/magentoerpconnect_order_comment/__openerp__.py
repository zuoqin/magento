# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: David BEAL Copyright 2014 Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
    'name': 'Magento Connector - Order comment',
    'version': '0.1',
    'category': 'Connector',
    'depends': ['magentoerpconnect',
                ],
    'author': 'MagentoERPconnect Core Editors',
    'license': 'AGPL-3',
    'website': 'http://www.odoo-magento-connector.com',
    'description': """
Sale order comments synchronisation
===================================

Extension for **Magento Connector**

Features
--------

* Import sale comments in the same time than 'sale order'
* Move messages from canceled order to replacing sale order (edited sale
  order in magento)
* Export messages from OpenERP sale order to Magento comment
* Export of moved messages to Magento

Settings / options
------------------

* Ability to require Magento to send email to customer for each comment
  received. Unactive by default (Connectors/Magento/Store menu).


    """,
    'images': [],
    'demo': [],
    'external_dependencies': {
        'python': ['bs4'],
    },
    'data': [
        'magento_model_view.xml',
    ],
    'installable': True,
    'application': False,
}
