# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

from sdeux.auto_detect import init_driver
from sdeux.serial_handler import S2SerialHandler

if __name__ == '__main__':
    th = S2SerialHandler('/dev/ttyUSB0')
    th.open()
    s2 = init_driver(th)
    s2.set_up()
    s2.advanced_mode = True
    s2.set_configuration(device_id=662)