import os
import time

from sdeux.updater.writer import FirmwareUpdater

fwu = FirmwareUpdater(port='/dev/ttyUSB0',
                      firmware_path='/home/danieldi/PycharmProjects/sdeux/sdeux/sw/S2_3838.bin',
                      stm32flash_path='/usr/local/bin/stm32flash',
                      new_firmware_version=3838,
                      hw_version=2005)
fwu.connect()
fwu.s2.reboot_to_bootloader()
time.sleep(2)

fwu.disconnect()
# fwu.upgrade()
