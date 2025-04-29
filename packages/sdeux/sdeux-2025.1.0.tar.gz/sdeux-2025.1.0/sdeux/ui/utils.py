import glob
import logging
import sys
import serial

import tkinter as tk
from tkinter import ttk
from sdeux.gen2005 import S2 as S2_gen2005


def mode_to_label(mode):
    if ':' in mode:
        mode = int(mode.split(':')[0])
    return S2_gen2005.PULSING_MODES_LABELS.get(mode, 0)


def set_color_label(widget, color):
    style = ttk.Style()
    style.configure(f"{color.title()}.TLabel", foreground=color)
    widget.configure(style=f"{color.title()}.TLabel")


def validate_spinbox_int(new_value):
    try:
        if new_value == '':
            return True
        int(new_value)
    except ValueError:
        return False
    return True


def validate_spinbox_float(new_value):
    try:
        if new_value == '':
            return True
        float(new_value)
    except ValueError:
        return False
    return True


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class ScrolledTextLogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        log_entry = self.format(record)
        self.widget.insert(tk.END, f"{log_entry}\n")
        self.widget.see(tk.END)
