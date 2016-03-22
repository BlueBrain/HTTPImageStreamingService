#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014-2015, Human Brain Project
#                          Cyrille Favreau <cyrille.favreau@epfl.ch>
#
# This file is part of RenderingResourceManager
# <https://github.com/BlueBrain/HTTPImageStreaming>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""
This module contains the class in charge of fetching images from remote rendering
resources.
"""

# pylint: disable=W0403
import requests
import base64
import json

import os
import custom_logging as log

from settings import HISS_IMAGEJPEG


class RestFrameGrabber(object):
    """
    Constructor
    :param uri URI from which the image should be fetched
    """
    def __init__(self, uri):
        self.counter = 0
        # Contains the default 'not found' image
        self.frame_not_found = open(os.path.dirname(__file__) +
                                    '/../resources/image_not_found.jpg', 'rb').read()
        self.uri = uri + HISS_IMAGEJPEG

    def get_frame(self):
        """
        Returns the current image generated by the remote rendering resource
        """
        try:
            response = requests.get(
                    url=self.uri, timeout=0.6, headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                json_image_b64 = json.loads(response.content)
                return base64.decodestring(json_image_b64['data'])
            response.close()
        except requests.exceptions.RequestException as e:
            log.error(str(e))
        return None
