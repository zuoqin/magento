# -*- coding: utf-8 -*-
#########################################################################
# Copyright (C) 2009  Sharoon Thomas, Open Labs Business solutions      #
# Copyright (C) 2011 Akretion Sébastien BEAU sebastien.beau@akretion.com#
# Copyright (C) 2013 Akretion Chafique DELLI chafique.delli@akretion.com#
#                                                                       #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################
import os

from openerp.osv import fields, orm
from openerp.tools.translate import _


class product_image(orm.Model):
    "Products Image gallery"
    _name = "product.image"
    _table = 'product_image'
    _inherits = {
        'image.image': 'image_id',
        }


    _columns = {
        'product_id' : fields.many2one(
            'product.product',
            string='Product'),
        'image_id' : fields.many2one(
            'image.image',
            string='Image',
            required=True,
            ondelete='cascade'),
        'sequence': fields.integer(
            'Sequence',
            help="The sequence number will use this to order the product images"),
    }

    _order = "sequence, image_id"

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        image_image_ids = []
        for image in self.browse(cr, uid, ids, context=context):
            #for now we don't check if there is several product_image for one image_image
            #if so this override has to be modified
            image_image_ids.append(image.image_id.id)
        #unlink image_image when product_image is deleted
        self.pool['image.image'].unlink(cr, uid, image_image_ids, context=context)
        return super(product_image, self).unlink(cr, uid, ids, context=context)
