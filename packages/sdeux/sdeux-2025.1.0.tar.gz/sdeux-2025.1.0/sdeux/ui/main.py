import argparse
import os
import tkinter as tk
import sys
from tkinter import ttk, scrolledtext

from sdeux.config import GUI_CONFIG, GUIConfiguration
from sdeux.ui.manager import GUIManager, UpgradeDialogManager
from sdeux.ui.utils import serial_ports, validate_spinbox_int, validate_spinbox_float


def main(config=GUI_CONFIG):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # When running as a bundled executable
        assets_dir = os.path.join(sys._MEIPASS, 'assets')
    else:
        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')

    window = tk.Tk()
    window.iconphoto(False, tk.PhotoImage(file=os.path.join(assets_dir, "icon.png")))
    g = GUIManager(config)
    window.title(f"{g.get_version()} - S-2m Control")
    g.set_screen_ratio((window.winfo_screenwidth() or 1920.0) / (1920.0 * 2))  # tested on 4k display
    window.columnconfigure([0, 2], weight=1, minsize=g.scale_screen(300))
    window.columnconfigure(1, weight=1, minsize=g.scale_screen(400))

    window.minsize(g.scale_screen(1200), g.scale_screen(1000))
    padx, pady = g.scale_screen(6), g.scale_screen(6)
    m = UpgradeDialogManager(g)

    # LOGO
    image_path = os.path.join(assets_dir, "logo.png")
    logo = tk.PhotoImage(file=image_path)
    logo_label = ttk.Label(window, image=logo)
    logo_label.grid(row=g.cur_row(), column=0, columnspan=3, pady=10)

    # PORT
    ttk.Label(window, text=f"Port:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')

    def scan_ports():
        ports = serial_ports()
        if ports:
            g.controls['opt_port']['values'] = ports
            g.widgets_vals['opt_port'].set(ports[0])

    def open_popup():
        popup = tk.Toplevel(window)
        popup.title("Upgrade Firmware")
        popup.iconphoto(False, tk.PhotoImage(file=os.path.join(assets_dir, "icon.png")))
        popup.grab_set()

        m.widgets_vals['message'] = tk.StringVar()
        ttk.Label(popup, textvariable=m.widgets_vals['message']).grid(row=0, column=0, columnspan=2, padx=padx, pady=pady)

        m.widgets_vals['fw_port'] = tk.StringVar()
        if g.controls['opt_port']['values']:
            m.widgets_vals['fw_port'].set(g.widgets_vals['opt_port'].get())
        m.widgets['fw_port'] = ttk.Combobox(popup, textvariable=m.widgets_vals['fw_port'], state="disabled")
        # m.widgets['fw_port']['values'] = g.controls['opt_port']['values']
        m.widgets['fw_port']['values'] = [g.widgets_vals['opt_port'].get()]
        m.widgets['fw_port'].grid(row=1, column=0, columnspan=2, padx=padx, pady=pady)

        m.widgets['upgrade_btn'] = ttk.Button(popup, text="UPGRADE", command=m.upgrade_fw)
        m.widgets['upgrade_btn'].grid(row=2, column=0, columnspan=2, padx=padx, pady=pady)

        m.widgets['log_textarea'] = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=60, height=12)
        m.widgets['log_textarea'].grid(row=3, column=0, columnspan=2, padx=padx, pady=pady)

        m.check_upgrade_allowed()

    verify_sb_int_cmd = (window.register(validate_spinbox_int), '%P')
    verify_sb_float_cmd = (window.register(validate_spinbox_float), '%P')

    frame = ttk.Frame(master=window, borderwidth=1)
    frame.grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')
    g.widgets_vals['opt_port'] = tk.StringVar()
    av_ports = serial_ports()
    if av_ports:
        g.widgets_vals['opt_port'].set(av_ports[0])
    g.controls['opt_port'] = ttk.Combobox(frame, textvariable=g.widgets_vals['opt_port'], state="readonly")
    g.controls['opt_port']['values'] = av_ports
    g.controls['opt_port'].grid(row=0, column=0)
    g.controls['btn_port'] = ttk.Button(frame, text=f"Scan", width=4, command=scan_ports)
    g.controls['btn_port'].grid(row=0, column=1, padx=padx)

    g.widgets['connect'] = ttk.Checkbutton(window, text="connect", variable=g.widgets_vals['connect'],
                                           command=lambda: g.connect_s2())
    g.widgets['connect'].grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # ACTUAL
    ttk.Label(window, text=f"Actual:").grid(row=g.next_row(), column=2, padx=padx, pady=pady, sticky='w')

    # PULSE PERIOD
    ttk.Label(window, text=f"Period [ns]:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')

    g.widgets_vals['pulse_period'].trace('w', g.update_duty_cycle)
    g.widgets['pulse_period'] = tk.Spinbox(window, from_=50, to=0xFFFFFFFF, increment=10, textvariable=g.widgets_vals['pulse_period'],
                   validatecommand=verify_sb_int_cmd, validate="key")
    g.widgets['pulse_period'].grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, textvariable=g.fields['pulse_period']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # FREQUENCY
    ttk.Label(window, text=f"Frequency [kHz]:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.widgets_vals['frequency']).grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.fields['frequency']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # PULSE WIDTH
    ttk.Label(window, text=f"Pulse Width [ns]:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')

    g.widgets_vals['pulse_width'].trace('w', g.update_duty_cycle)
    tk.Spinbox(window, from_=0, to=0xFFFFFFFF, increment=10, textvariable=g.widgets_vals['pulse_width'],
               validatecommand=verify_sb_int_cmd, validate="key")\
                .grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, textvariable=g.fields['pulse_width']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # DUTY CYCLE
    ttk.Label(window, text=f"Duty Cycle [%]:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.widgets_vals['duty_cycle']).grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.fields['duty_cycle']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # MODE DEPENDANT FIELDS
    if g.is_public_release():
        fields = {'output_voltage': "Output Voltage [V]:", 'gating_voltage': "Gating Voltage [V]:",
                  'gating_pulse_width': "Gating Pulse Width [ns]:", 'peak_current_limit': "Peak Current Limit [A]:",
                  'nb_pulses': "Nb. of Pulses:"}
    else:
        fields = {'output_voltage': "Output Voltage [V]:", 'output_voltage_a': "Output Voltage A [V]:",
                  'pulse_width_a': "Pulse Width A [ns]:", 'output_voltage_b': "Output Voltage B [V]:",
                  'pulse_width_b': "Pulse Width B [ns]:", 'peak_current_limit': "Peak Current Limit [A]:"}

    for field in fields:
        g.widgets_vals[field] = tk.StringVar()
        g.fields[field] = tk.StringVar()
        ttk.Label(master=window, text=fields[field]).grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')

        if 'width' in field or field == 'nb_pulses':
            g.widgets[field] = tk.Spinbox(window, from_=0, to=0xFFFFFFFF, increment=10, textvariable=g.widgets_vals[field],
                                          validatecommand=verify_sb_int_cmd, validate="key")
        else:
            g.widgets[field] = tk.Spinbox(window, from_=0.0, to=0xFFFFFFFF, increment=.01, textvariable=g.widgets_vals[field],
                                          validatecommand=verify_sb_float_cmd, validate="key")
        g.widgets[field].grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')

        ttk.Label(window, textvariable=g.fields[field]).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # OUTPUT MODE
    ttk.Label(master=window, text=f"Output Mode:").grid(row=g.next_row(), column=0, padx=padx, pady=pady, sticky='w')

    om_vals = g.get_om_vals()
    g.widgets_vals['output_mode'].set(om_vals[0])
    cb_om = ttk.Combobox(window, textvariable=g.widgets_vals['output_mode'], state="readonly")
    g.widgets_vals['output_mode'].trace('w', g.set_readonly_fields)
    cb_om['values'] = om_vals
    cb_om.grid(row=g.cur_row(), column=1, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, textvariable=g.fields['output_mode']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    # CONTROLS
    frame = ttk.Frame(master=window, borderwidth=1)
    frame.grid(row=g.next_row(), column=2, padx=padx, pady=pady, sticky='w')
    g.controls['btn_apply'] = ttk.Button(master=frame, text=f"Apply", width=6, command=g.apply, state='disabled')
    g.controls['btn_apply'].grid(row=0, column=0)
    g.controls['btn_store'] = ttk.Button(master=frame, text=f"Store", width=6, command=lambda: g.apply(True), state='disabled')
    g.controls['btn_store'].grid(row=0, column=1, padx=padx)

    boldStyle = ttk.Style()
    boldStyle.configure("Bold.TButton", font=('Sans', '13', 'bold'), foreground='red')
    g.controls['btn_stop'] = ttk.Button(master=window, text=f"STOP", command=g.stop, state='disabled', style="Bold.TButton")
    g.controls['btn_stop'].grid(row=g.next_row(), column=0, columnspan=3, padx=padx, pady=pady, sticky='we')

    # STATUS
    ttk.Label(window, text=f"Board Status:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    frame = ttk.Frame(master=window, borderwidth=1)
    frame.grid(row=g.cur_row(), column=2, sticky='w')
    g.widgets['board_status'] = ttk.Label(frame, textvariable=g.status_fields['board_status'])
    g.widgets['board_status'].grid(row=0, column=0, padx=padx, pady=pady, sticky='w')
    g.controls['btn_reset_flags'] = ttk.Button(frame, text=f"Reset", width=5, command=g.reset_flags, state='disabled')

    ttk.Label(window, text=f"Power supply voltage [V]:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['power_supply_voltage']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, text=f"Pulse current [A]:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['pulse_current']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, text=f"Board temperature [°C]:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['board_temperature']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, text=f"Device ID:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['device_id']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, text=f"Hardware version:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['hw_version']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    ttk.Label(window, text=f"Firmware version:").grid(row=g.next_row(), column=0, columnspan=2, padx=padx, pady=pady, sticky='w')
    ttk.Label(window, textvariable=g.status_fields['fw_version']).grid(row=g.cur_row(), column=2, padx=padx, pady=pady, sticky='w')

    if g.config.upgrade_allowed:
        g.controls['btn_upgrade_fw'] = ttk.Button(master=window, text=f"UPGRADE FIRMWARE", command=open_popup)
        g.controls['btn_upgrade_fw'].grid(row=g.next_row(), column=0, columnspan=3, padx=padx, pady=pady, sticky='we')

    g.set_readonly_fields(0, 0, 0)
    g.set_widgets_data()

    def on_closing():
        g.disconnect_s2()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--upgrade-firmware', action='store_true', default=False,
                        help='Add this option if you want to allow firmware upgrade via the GUI')
    parser.add_argument('--firmware-version', type=int,
                        help='The firmware version the can be installed via the GUI, ignored if --upgrade-firmware is set to false')
    parser.add_argument('--release-type', type=str,
                        help='The release type, use "public" if you want the GUI with less options')
    args = parser.parse_args()
    if not args.upgrade_firmware and not args.firmware_version and not args.release_type:
        main()
    else:
        gui_conf = GUIConfiguration(upgrade_allowed=args.upgrade_firmware, firmware_version=args.firmware_version,
                                    release_type=args.release_type)
        main(gui_conf)
