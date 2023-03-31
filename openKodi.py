import pyudev
from multiprocessing import Process
import os

WATCH_FILE = '/sys/class/drm/card0-HDMI-A-1/edid'
WAIT_TIME  = 5

PROC_PID = -1

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('drm')
device = pyudev.Devices.from_path(context, '/sys/class/drm/card0-HDMI-A-1')
# device = pyudev.Devices.from_path(context, '/sys/class/drm/card0-HDMI-A-1')[0]



def open_kodi():
    os.popen('kodi')


def handle_event(observer, device):
    global PROC_PID
    #if device.sys_path == '/sys/class/drm/card0-HDMI-A-1/edid':
    print('El archivo /sys/class/drm/card0-HDMI-A-1/edid ha sido modificado')
    # Leer el contenido del archivo
    with open(WATCH_FILE, "rb") as f:
        content = f.read()
        # print(content)
        if content:
            print ("ENCENDIDO")
            if PROC_PID == -1:
                print ('Imos inicialo')
                p = Process(target=open_kodi)
                p.start()
                PROC_PID = p.pid
                print ('INICIADO')
        else:
            print ("APAGADO")
            if PROC_PID != -1:
                os.popen(['kill', PROC_PID])
            PROC_PID = -1
            print ('KILL FEITO')

with open(WATCH_FILE, "rb") as f:
        content = f.read()
        print ('ESTADO ACTUAL:', 'encendido' if content else 'apagado')

observer = pyudev.MonitorObserver(monitor, handle_event)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()
