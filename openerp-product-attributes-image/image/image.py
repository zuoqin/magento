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
import base64
import urllib
import os
import re

from openerp.osv import fields, orm, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

IMAGE_PER_FOLDER = 500

#TODO find a good solution in order to roll back changed done on file system
#TODO add the possibility to move from a store system to an other
# (example : moving existing image on database to file system)


class image_image(orm.Model):
    "Image gallery"
    _name = "image.image"
    _description = __doc__

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for image in self.browse(cr, uid, ids, context=context):
            full_path = self._get_image_full_path(cr, uid, image,
                                                  context=context)
            if full_path:
                os.path.isfile(full_path) and os.remove(full_path)
        return super(image_image, self).unlink(cr, uid, ids, context=context)

    def create(self, cr, uid, vals, context=None):
        if vals.get('name') and not vals.get('extension'):
            vals['name'], vals['extension'] = os.path.splitext(vals['name'])
            vals['name'] = re.sub(r'[?%*:|\"<>]','', vals['name'])
            vals['label'] = vals['name'].replace('_', ' ').capitalize()
        return super(image_image, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        if vals.get('name') and not vals.get('extension'):
            vals['name'], vals['extension'] = os.path.splitext(vals['name'])
        upd_ids = ids[:]
        if vals.get('name') or vals.get('extension'):
            images = self.browse(cr, uid, upd_ids, context=context)
            for image in images:
                old_full_path = self._get_image_full_path(cr, uid, image,
                                                          context=context)
                if not old_full_path:
                    continue
                # all the stuff below is there to manage
                # the files on the filesystem
                if vals.get('name') and (image.name != vals['name']) \
                        or vals.get('extension') \
                        and (image.extension != vals['extension']):
                    super(image_image, self).write(
                        cr, uid, image.id, vals, context=context)
                    upd_ids.remove(image.id)
                    if 'file' in vals:
                        # a new image have been loaded we should
                        # remove the old image
                        # TODO it's look like there is something wrong
                        # with function field in openerp indeed
                        # the preview is always added in the write :(
                        if os.path.isfile(old_full_path):
                            os.remove(old_full_path)
                    else:
                        new_image = self.browse(cr, uid, image.id,
                                                context=context)
                        new_full_path = self._get_image_full_path(
                            cr, uid, new_image, context=context)
                        #we have to rename the image on the file system
                        if os.path.isfile(old_full_path):
                            os.rename(old_full_path, new_full_path)
        return super(image_image, self).write(cr, uid, upd_ids, vals,
                                              context=context)

    def _get_image_full_path(self, cr, uid, image, context=None):
        if self._use_filesystem(cr, uid, context=context):
            base_path = self._get_image_base_path(cr, uid, context=context)
            base_index = image.id-image.id%IMAGE_PER_FOLDER
            folder_name = "%s-%s"%(base_index + 1,
                                   base_index + IMAGE_PER_FOLDER)
            full_path = os.path.join(
                    base_path,
                    folder_name,
                    '%s%s' % (image.id, image.extension or ''))
        else:
            full_path = False
        return full_path

    def _use_filesystem(self, cr, uid, context=None):
        if self._get_image_base_path(cr, uid, context=context):
            return True
        return False

    def _get_image_base_path(self, cr, uid, context=None):
        config_parameter_obj = self.pool.get('ir.config_parameter')
        path = config_parameter_obj.get_param(cr, uid, 'image.store_path',
                                              context=context)
        if path == 'False':
            return False
        return path

    def get_image(self, cr, uid, id, context=None):
        image = self.browse(cr, uid, id, context=context)
        if image.link:
            if image.url:
                (filename, header) = urllib.urlretrieve(image.url)
                with open(filename, 'rb') as f:
                    img = base64.b64encode(f.read())
            else:
                return False
        else:
            full_path = self._get_image_full_path(cr, uid, image, context=context)
            if full_path:
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'rb') as f:
                            img = base64.b64encode(f.read())
                    except Exception, e:
                        _logger.error("Can not open the image %s, error : %s",
                                      full_path, e, exc_info=True)
                        return False
                else:
                    _logger.error("The image %s doesn't exist ", full_path)
                    return False
            else:
                img = image.file_db_store
        return img

    def _get_image(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for each in ids:
            res[each] = self.get_image(cr, uid, each, context=context)
        return res

    def _check_filestore(self, image_filestore):
        """check if the filestore is created, if not it create it
        automatically
        """
        try:
            dir_path = os.path.dirname(image_filestore)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        except OSError, e:
            raise osv.except_osv(
                    _('Error'),
                    _('The image filestore can not be created, %s') % e)
        return True

    def _save_file(self, path, b64_file):
        """Save a file encoded in base 64"""
        self._check_filestore(path)
        with open(path, 'w') as ofile:
            ofile.write(base64.b64decode(b64_file))
        return True

    def _set_image(self, cr, uid, id, name, value, arg, context=None):
        image = self.browse(cr, uid, id, context=context)
        full_path = self._get_image_full_path(cr, uid, image, context=context)
        if full_path:
            return self._save_file(full_path, value)
        return self.write(cr, uid, id, {'file_db_store': value},
                          context=context)

    _columns = {
        'name': fields.char(
            'Name',
            required=True,
            help="File name"),
        'label': fields.char(
            'Image label',
            translate=True,
            size=64,
            help=""),
        'extension': fields.char(
            'File extension',
            readonly=True,
            oldname='extention'),
        'link': fields.boolean('Link?',
            help="Images can be linked from files on "
                 "your file system or remote (Preferred)"),
        'file_db_store': fields.binary('Image stored in database'),
        'file': fields.function(_get_image,
                                fnct_inv=_set_image,
                                type="binary",
                                string="File",
                                filters='*.png,*.jpg,*.gif'),
        'url': fields.char(
            'File Location',
            help="URL"),
        'comments': fields.text('Comments'),
        }

    _defaults = {
        'link': False,
        }
