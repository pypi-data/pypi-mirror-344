import logging
import os
import requests

from sdeux.updater.writer import FirmwareUpdater


def download_firmware(fw_url):
    fw = requests.get(fw_url)
    file_path = os.path.join('/tmp/', fw_url.split('/')[-1])
    with open(file_path,
              'wb') as f:
        f.write(fw.content)
    return file_path

def get_firmware(version):
    rsp = requests.get('http://s2admin/api/s2firmware',
                       params={'version': version})
    rsp.raise_for_status()
    d = rsp.json()
    if not d:
        return None
    if len(d) == 1:
        return d[0]
    raise Exception('expected exactly one firmware with version={}, '
                    'but {} was found'.format(version, d))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    s2_port = '/dev/ttyUSB0'
    fw_info = get_firmware(3835)
    fw_path = download_firmware(fw_info['binary_file'])
    fu = FirmwareUpdater(port=s2_port,
                         device_serial=662,
                         firmware_path=fw_path,
                         stm32flash_path='/usr/local/bin/stm32flash',
                         new_firmware_version=3835,#s2_fw_version,
                         hw_version=2005,
                         configuration=dict(mode_auto_duty_limit_low=0.25,
                                            mode_auto_duty_limit_high=0.30)
                         )
    fu.install()