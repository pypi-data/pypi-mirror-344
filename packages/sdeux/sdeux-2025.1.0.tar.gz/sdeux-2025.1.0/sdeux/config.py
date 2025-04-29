# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"


import os

FIRMWARES_DIR_PATH = os.path.join(os.path.dirname(__file__),
                                  'sw')


class GUIConfiguration:

    def __init__(self, upgrade_allowed, firmware_version, release_type='public', max_voltage=25):
        self.upgrade_allowed = upgrade_allowed
        self.firmware_version = firmware_version
        self.release_type = release_type
        self.max_voltage = max_voltage


GUI_CONFIG = GUIConfiguration(True, 4003,  'public')
