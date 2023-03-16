import pyudev

WATCH_FILE = '/sys/class/drm/card0-HDMI-A-1/edid'
WAIT_TIME  = 5

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('drm')
device = pyudev.Devices.from_path(context, '/sys/class/drm/card0-HDMI-A-1')

def handle_event(observer, device):
    #if device.sys_path == '/sys/class/drm/card0-HDMI-A-1/edid':
    print('El archivo /sys/class/drm/card0-HDMI-A-1/edid ha sido modificado')
    # Leer el contenido del archivo
    with open(WATCH_FILE, "rb") as f:
        content = f.read()
        # print(content)
        if content:
            print ("ENCENDIDO")
        else:
            print ("APAGADO")

observer = pyudev.MonitorObserver(monitor, handle_event)
observer.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()
