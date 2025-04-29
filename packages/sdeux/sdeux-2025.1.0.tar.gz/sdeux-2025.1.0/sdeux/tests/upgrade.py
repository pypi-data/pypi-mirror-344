import logging
import os
import sys
from logging import StreamHandler

from sdeux.updater.writer import FirmwareUpdater, terminalLogger, logger

terminalLogger.setLevel(logging.INFO)
lsh = StreamHandler(stream=sys.stdout)
terminalLogger.addHandler(lsh)
fwu = FirmwareUpdater(port='/dev/ttyUSB0',
                      firmware_path='/home/danieldi/PycharmProjects/sdeux/sdeux/sw/S2_3838.bin',
                      stm32flash_path='/home/danieldi/PycharmProjects/sdeux/sdeux/ui/stm32flash/stm32flash',
                      new_firmware_version=3838,
                      hw_version=2005)
fwu.upgrade()
