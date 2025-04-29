import logging
import os
import time
import tkinter as tk
from tkinter import messagebox

import sys
import threading

from sdeux.gen2005 import S2 as S2_gen2005
from sdeux.communication import RETRY_SOME
from sdeux.serial_handler import S2SerialHandler
from sdeux.ui.utils import mode_to_label, set_color_label, ScrolledTextLogHandler
from sdeux.updater.writer import FirmwareUpdater, terminalLogger, logger

SETTINGS_MAP = {
    'output_mode': {'fields': ['pulsing_mode'], 'func': mode_to_label},
    'pulse_period': {'fields': ['pulse_period'], 'func': int},
    'pulse_width': {'fields': ['pulse_width'], 'func': int},
    'output_voltage': {'fields': ['voltage'], 'func': float},
    'output_voltage_a': {'fields': ['voltage_A'], 'func': float},
    'output_voltage_b': {'fields': ['voltage_B'], 'func': float},
    'pulse_width_a': {'fields': ['pulse_width_A'], 'func': float},
    'pulse_width_b': {'fields': ['pulse_width_B'], 'func': float},
    'gating_voltage': {'fields': ['voltage_A', 'voltage_B'], 'func': float},
    'gating_pulse_width': {'fields': ['pulse_width_A', 'pulse_width_B'], 'func': float},
    'peak_current_limit': {'fields': ['current_limit'], 'func': float},
    'nb_pulses': {'fields': ['external_trigger_pulse_repetitions'], 'func': int}
}

READONLY_MAP = {'output_voltage': [0, 4, 5, 8, 9, 10, 11],
                'output_voltage_a': [0, 1, 5, 6, 7, 12, 13, 9, 10, 11],
                'pulse_width_a': [0, 1, 4, 5, 6, 7, 12, 13, 9, 10, 11],
                'output_voltage_b': [0, 1, 2, 4, 6, 7, 12, 13],
                'pulse_width_b': [0, 1, 4, 5, 6, 7, 12, 13, 9, 10, 11],
                'gating_voltage': [0, 1, 6, 7],
                'gating_pulse_width': [0, 1, 6, 7],
                'nb_pulses': [0, 1, 7],
                }


class GUIManager:
    def __init__(self, gui_config):
        self.s2 = None
        self._screen_ratio = 1.0
        self._row = 0
        self._public = gui_config.release_type == 'public'
        self._gui_version = '4003.1'
        self._refresh_thread = None
        self._stop_thread = threading.Event()
        self._lock = threading.Lock()
        self.th = None
        self.config = gui_config
        self.widgets = {}
        self.controls = {}
        self.fields = {'pulse_period': tk.StringVar(), 'frequency': tk.StringVar(), 'pulse_width': tk.StringVar(),
                       'duty_cycle': tk.StringVar(), 'output_voltage': tk.StringVar(), 'output_mode': tk.StringVar()}
        self.status_fields = {'board_status': tk.StringVar(), 'power_supply_voltage': tk.StringVar(),
                              'pulse_current': tk.StringVar(), 'board_temperature': tk.StringVar(),
                              'device_id': tk.StringVar(), 'hw_version': tk.StringVar(), 'fw_version': tk.StringVar()}
        self.widgets_vals = {'pulse_period': tk.StringVar(), 'frequency': tk.StringVar(), 'pulse_width': tk.StringVar(),
                             'duty_cycle': tk.StringVar(), 'output_voltage': tk.StringVar(), 'output_mode': tk.StringVar(),
                             'connect': tk.BooleanVar()}
        threading.Thread(target=self._refresh_ui, daemon=True).start()

    def set_screen_ratio(self, val):
        self._screen_ratio = val

    def scale_screen(self, val):
        return int(self._screen_ratio * val)

    def next_row(self):
        self._row += 1
        return self._row

    def cur_row(self):
        return self._row

    def is_public_release(self):
        return self._public

    def get_version(self):
        return self._gui_version

    def connect_s2(self):
        try:
            conn = self.widgets_vals['connect'].get()
            if not conn:
                self.disconnect_s2()
                return
            if self.th is not None and self.th.is_open():
                self.th.close()
            self.th = S2SerialHandler(self.widgets_vals['opt_port'].get())
            if not self.th.is_open():
                self.th.open()
            self.s2 = S2_gen2005(self.th, max_voltage=self.config.max_voltage)
            self.s2.retry_policy = RETRY_SOME
            try:
                self.s2.reload_settings(expected_response_time=1.0)
            except Exception:
                messagebox.showerror("Error", "Connection error, please check serial port and retry")
                self.disconnect_s2()
                return
            with self._lock:
                if self._refresh_thread is not None and self._refresh_thread.is_alive():
                    return
                self._stop_thread.clear()
                self._refresh_thread = threading.Thread(target=self._refresh_data)
                self._refresh_thread.start()
                self.set_controls_state(True)
        except Exception as e:
            self.disconnect_s2()
            messagebox.showerror("Error", str(e))

    def disconnect_s2(self):
        with self._lock:
            self._stop_thread.set()
            refresh_thread = self._refresh_thread
            self._refresh_thread = None

        if refresh_thread is not None:
            refresh_thread.join()
            # print("Thread joined")

        self.widgets_vals['connect'].set(False)
        self.set_controls_state(False)

    def _refresh_data(self):
        x = 0
        while not self._stop_thread.is_set():
            try:
                self._reload_all()
                if x == 0:
                    self.set_widgets_data(s2_data=True)
                    x = 1
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.widgets_vals['connect'].set(False)
                self.set_controls_state(False)
                self.th.close()
                break
            for _ in range(10):
                if self._stop_thread.is_set():
                    break
                time.sleep(0.05)

    def _refresh_ui(self):
        while True:
            if self._refresh_thread and self._refresh_thread.is_alive() and self.s2:
                self.set_actual_values()
                if self.s2.status_register.hasErrors:
                    self.controls['btn_reset_flags'].config(state='normal')
                    set_color_label(self.widgets['board_status'], 'red')
                else:
                    self.controls['btn_reset_flags'].config(state='disabled')
                    set_color_label(self.widgets['board_status'], 'black')
                # print('Values set...')
            time.sleep(0.3)

    def get_om_vals(self):
        if self.is_public_release():
            return ['0: Off', '1: Pulsing', '6: Burst External Trigger', '7: External Trigger', '8: External Gating']
        return ['0: Off', '1: Pulsing', '4: Mode A', '5: Mode B', '7: External Trigger', '8: A/B Auto',
                '12: Mode C Steady-State', '13: Mode C Short-Time', '9: B4', '10: B6', '11: B8']

    def set_controls_state(self, connect):
        self.controls['opt_port'].config(state='disabled' if connect else 'readonly')
        self.controls['btn_port'].config(state='disabled' if connect else 'normal')
        self.controls['btn_apply'].config(state='normal' if connect else 'disabled')
        self.controls['btn_store'].config(state='normal' if connect else 'disabled')
        self.controls['btn_stop'].config(state='normal' if connect else 'disabled')
        if not connect:
            self.controls['btn_reset_flags'].grid_remove()
        else:
            self.controls['btn_reset_flags'].grid(row=0, column=1, padx=self.scale_screen(6),
                                                  pady=self.scale_screen(6), sticky='w')

    def set_actual_values(self):
        try:
            self.fields['pulse_period'].set(f'{int(self.s2.pulse_period)}')
            self.fields['frequency'].set(f'{int(1e6 / int(self.s2.pulse_period))}')
            self.widgets_vals['frequency'].set(f'{int(1e6 / int(self.s2.pulse_period))}')
            self.fields['pulse_width'].set(f'{int(self.s2.pulse_width)}')
            self.fields['output_voltage'].set(f'{float(self.s2.settings.output_voltage_set):.2f} / '
                                              f'{float(self.s2.info.output_voltage_measured):.2f}')
            if self.is_public_release():
                self.fields['gating_voltage'].set(f'{float(self.s2.settings.output_voltage_set_A):.2f} / '
                                                  f'{float(self.s2.info.output_voltage_measured):.2f}')
                self.fields['gating_pulse_width'].set(f'{int(self.s2.settings.pulse_width_A * 10)}')
                self.fields['nb_pulses'].set(f'{int(self.s2.external_trigger_pulse_repetitions)}')
            else:
                self.fields['output_voltage_a'].set(f'{float(self.s2.settings.output_voltage_set_A):.2f} / '
                                                    f'{float(self.s2.info.output_voltage_measured):.2f}')
                self.fields['pulse_width_a'].set(f'{int(self.s2.settings.pulse_width_A * 10)}')
                self.fields['output_voltage_b'].set(f'{float(self.s2.settings.output_voltage_set_B):.2f} / '
                                                    f'{float(self.s2.info.output_voltage_measured):.2f}')
                self.fields['pulse_width_b'].set(f'{int(self.s2.settings.pulse_width_B * 10)}')
            self.fields['peak_current_limit'].set(f'{float(self.s2.settings.output_current_limit):.2f}')
            self.fields['output_mode'].set(f'{int(self.s2.settings.pulsing_mode)}')

            bs = self.s2.status_register.to_user_message().split(':')[-1].strip()
            self.status_fields['board_status'].set(bs)
            self.status_fields['power_supply_voltage'].set(f'{self.s2.info.input_voltage_measured:.1f}')
            self.status_fields['pulse_current'].set(f'{float(self.s2.info.output_current_measured):.3f}')
            self.status_fields['board_temperature'].set(f'{round(self.s2.info.MCU_temperature)}')
            self.status_fields['device_id'].set(self.s2.info.device_id)
            self.status_fields['hw_version'].set(self.s2.info.hw_version)
            self.status_fields['fw_version'].set(self.s2.info.sw_version)
        except AttributeError:
            print('ERROR while setting field')

    def set_widgets_data(self, s2_data=False):
        self.widgets_vals['pulse_period'].set(f'{int(self.s2.pulse_period) if s2_data else 5000}')
        pp = int(self.widgets_vals['pulse_period'].get())
        self.widgets_vals['frequency'].set(f'{int(1e6 / pp)}')
        self.widgets_vals['pulse_width'].set(f'{int(self.s2.pulse_width) if s2_data else 10}')
        self.update_duty_cycle(0, 0, 0)
        val = f'{float(self.s2.settings.output_voltage_set):.2f}' if s2_data else 0.00
        self.widgets_vals['output_voltage'].set(f'{val}')
        if self.is_public_release():
            val = f'{float(self.s2.settings.output_voltage_set_A):.2f}' if s2_data else 0.00
            self.widgets_vals['gating_voltage'].set(f'{val}')
            self.widgets_vals['gating_pulse_width'].set(f'{int(self.s2.settings.pulse_width_A * 10) if s2_data else 10}')
            val = f'{int(self.s2.external_trigger_pulse_repetitions)}' if s2_data else 0
            self.widgets_vals['nb_pulses'].set(f'{val}')
        else:
            val = f'{float(self.s2.settings.output_voltage_set_A):.2f}' if s2_data else 0.00
            self.widgets_vals['output_voltage_a'].set(f'{val}')
            self.widgets_vals['pulse_width_a'].set(f'{int(self.s2.settings.pulse_width_A * 10) if s2_data else 10}')
            val = f'{float(self.s2.settings.output_voltage_set_B):.2f}' if s2_data else 0.00
            self.widgets_vals['output_voltage_b'].set(f'{val}')
            self.widgets_vals['pulse_width_b'].set(f'{int(self.s2.settings.pulse_width_B * 10) if s2_data else 10}')
        val = f'{float(self.s2.settings.output_current_limit):.2f}' if s2_data else 0.00
        self.widgets_vals['peak_current_limit'].set(f'{val}')
        if s2_data:
            val = [x for x in self.get_om_vals() if str(self.s2.settings.pulsing_mode) == x.split(':')[0]]
            if val:
                self.widgets_vals['output_mode'].set(val[0])

    def _reload_all(self):
        self.s2.reload_info(expected_response_time=1.0)
        self.s2.reload_settings(expected_response_time=1.0)

    def _apply(self, store=False):
        if not self.s2:
            return
        settings = {}
        for field in self.widgets_vals:
            if field == 'output_mode':
                mode = int(self.widgets_vals[field].get().split(':')[0])
                if mode in (6, 7) and int(self.status_fields['device_id'].get()) < 700:
                    messagebox.showerror("Error", "External Trigger modes not available for this S-2m")
                    return
            if field in SETTINGS_MAP:
                for f in SETTINGS_MAP[field]['fields']:
                    if 'func' in SETTINGS_MAP[field]:
                        settings[f] = SETTINGS_MAP[field].get('func')(self.widgets_vals[field].get() or 0)
        settings['persistent'] = store
        self.s2.set_settings(**settings)

    def apply(self, store=False):
        self._apply(store=store)

    def store(self):
        self.apply(store=True)

    def stop(self):
        self.disconnect_s2()
        self.s2.shut_down()

    def reset_flags(self):
        self.s2.reset_overcurrent_flag()
        self.s2.reset_undervoltage_flag()
        self.s2.reset_overvoltage_flag()
        self.s2.reset_overtemp_flag()

    def update_duty_cycle(self, a, b, c):
        pw, pp = int(self.widgets_vals['pulse_width'].get() or 0), int(self.widgets_vals['pulse_period'].get() or 50)
        dc = min(100.0, pw / pp * 100 if pp else float(self.widgets_vals['duty_cycle'].get()))
        self.widgets_vals['duty_cycle'].set(f'{dc:.2f}')

    def set_readonly_fields(self, a, b, c):
        mode = int(self.widgets_vals['output_mode'].get().split(':')[0])
        for field_name in [x for x in READONLY_MAP if x in self.widgets]:
            if mode in READONLY_MAP[field_name]:
                self.widgets[field_name].config(state='readonly')
            else:
                self.widgets[field_name].config(state='normal')


class UpgradeDialogManager:
    def __init__(self, gui_manager):
        self._gui_manager = gui_manager
        self.widgets = {}
        self.widgets_vals = {'fw_port': tk.StringVar(), 'message': tk.StringVar()}

    def check_upgrade_allowed(self):
        ctrl_state = 'disabled'
        if not self._gui_manager._refresh_thread or not self._gui_manager._refresh_thread.is_alive():
            self.widgets_vals['message'].set('Cannot check firmware version. Please connect to the S-2m first.')
        elif self._gui_manager.s2.info.hw_version != 2005:
            self.widgets_vals['message'].set('The upgrade is only available for S-2m (hardware revision 2005).')
        elif int(self._gui_manager.s2.info.sw_version) == int(self._gui_manager.config.firmware_version):
            self.widgets_vals['message'].set('The firmware is already on the latest version.')
        else:
            self.widgets_vals['message'].set(f'Upgrade to version {self._gui_manager.config.firmware_version} OK')
            ctrl_state = 'normal'
        self.widgets['upgrade_btn'].config(state=ctrl_state)

    def _perform_upgrade(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # When running as a bundled executable
            firmware_dir = os.path.join(sys._MEIPASS, 'bin')
            stm32flash_dir = os.path.join(sys._MEIPASS, 'bin')
        else:
            firmware_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'sw')
            stm32flash_dir = os.path.join(os.path.dirname(__file__), 'stm32flash')
        terminalLogger.setLevel(logging.INFO)
        lsh = ScrolledTextLogHandler(self.widgets['log_textarea'])
        terminalLogger.addHandler(lsh)
        self.widgets_vals['message'].set('Upgrading... DO NOT disconnect S-2m or close the window!')
        self.widgets['upgrade_btn'].config(state='disabled')
        self.widgets['fw_port'].config(state='disabled')
        self._gui_manager.disconnect_s2()
        if self._gui_manager.th.is_open:
            self._gui_manager.th.close()
        port = S2SerialHandler(self.widgets_vals['fw_port'].get())
        if port.is_open:
            port.close()
        try:
            fwu = FirmwareUpdater(port=self.widgets_vals['fw_port'].get(),
                                  firmware_path=os.path.join(firmware_dir, f'S2_{self._gui_manager.config.firmware_version}.bin'),
                                  stm32flash_path=os.path.join(stm32flash_dir, 'stm32flash.exe' if os.name == 'nt' else 'stm32flash'),
                                  new_firmware_version=self._gui_manager.config.firmware_version,
                                  hw_version=2005)

            fwu.upgrade()
            self.widgets_vals['message'].set(
                f'Firmware upgraded to version {self._gui_manager.config.firmware_version}')
        except Exception as e:
            terminalLogger.error('Unexpected error executing the updater: {}'.format(e))

    def upgrade_fw(self):
        upgrade_thread = threading.Thread(target=self._perform_upgrade)
        upgrade_thread.start()
