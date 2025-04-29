import os

from sdeux.updater.writer import FirmwareUpdater

fwu = FirmwareUpdater(port='/dev/ttyUSB0',
                      firmware_path='/home/danieldi/PycharmProjects/sdeux/sdeux/sw/S2_3836.bin',
                      stm32flash_path='/usr/local/bin/stm32flash',
                      new_firmware_version=3836,
                      hw_version=2005,
                      device_serial='373')
fwu.install(True)
