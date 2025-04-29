# -*- coding: utf-8 -*-
"""
Created by chiesa

Copyright Alpes Lasers SA, Switzerland
"""
__author__ = 'chiesa'
__copyright__ = "Copyright Alpes Lasers SA"

import logging
import os
import sys
import time
from argparse import ArgumentParser
from glob import glob
from logging import FileHandler, Formatter, StreamHandler

from sdeux.updater.writer import terminalLogger, FirmwareUpdater


FIRMWARE_FOLDER = '/home/pi/updater/firmwares'


def main():
    parser = ArgumentParser()
    parser.add_argument('firmware', type=int,
                        help='the firmware number. The firmware file has to be stored in '
                             'the {} folder.'.format(FIRMWARE_FOLDER))
    parser.add_argument('--dev', type=str,
                        help='path to s2 device, i.e. /dev/ttyUSB1')
    args = parser.parse_args()
    firmware = args.firmware
    device_path = args.dev
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    try:
        lfh = FileHandler(filename=os.path.expanduser('~/s2updater.log'))
        lfh.setFormatter(Formatter(fmt='{asctime}:{levelname}: {message}', style='{'))
        lfh.setLevel(logging.INFO)
        rootLogger.addHandler(lfh)
        lsh = StreamHandler(stream=sys.stdout)
        terminalLogger.addHandler(lsh)

        firmware_path = os.path.join(FIRMWARE_FOLDER,
                                     's2_2005_{}_signed.bin'.format(firmware))

        if not os.path.exists(firmware_path):
            terminalLogger.info('Cannot find firmware {}'.format(firmware_path))
            sys.exit(1)

        if not device_path:
            devices = list(glob('/dev/tty.CHIPIX-*')) + list(glob('/dev/tty.USBCOM-*'))

            if len(devices) == 0:
                terminalLogger.info('Could not find any Chipi-X or USBCOM connected. Please connect one.')
                sys.exit(1)

            if len(devices) > 1:
                terminalLogger.info('More than one Chipi-X or USBCOM are connected. Please connect only one.')
                sys.exit(1)
            device_path = devices[0]

        fwu = FirmwareUpdater(port=device_path,
                              firmware_path=firmware_path,
                              stm32flash_path='/usr/bin/stm32flash',
                              new_firmware_version=firmware,
                              hw_version=2005,
                              configuration=dict(mode_auto_duty_limit_low=0.25,
                                                 mode_auto_duty_limit_high=0.30))

        terminalLogger.info('Please connect S2 for update')

        while True:
            if fwu.is_connected():
                break
            time.sleep(1.0)

        fwu.upgrade()
    except Exception as e:
        rootLogger.exception(e)
        terminalLogger.error('Unexpected error executing the updater: {}'.format(e))


if __name__ == '__main__':
    main()
