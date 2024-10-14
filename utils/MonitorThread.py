from gui.mainWindow import *
import os
import time
import wmi


class MonitorThread(QThread):
    output = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        c = wmi.WMI()
        usb_watcher = c.Win32_USBHub.watch_for("creation")
        usb_remover = c.Win32_USBHub.watch_for("deletion")
        device_connect = usb_watcher()
        if device_connect:
            print(f"Device connected: {device_connect.DeviceID}")
            self.output.emit(str(device_connect.DeviceID))

        device_disconnect = usb_remover()
        if device_connect:
            dis_tips = f'{device_disconnect.deviceID} is Disconnected'
            self.output.emit(dis_tips)
