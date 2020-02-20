import usb
import universal_serial_bus

from universal_serial_bus import *


print(usb.core.show_devices(verbose = False))

# idVendor = 1118
# idProduct = 1915

# idVendor = 0x8086
# idProduct = 0xa12f

# dev = usb.core.find(idVendor = idVendor, idProduct = idProduct)
# dev = universal_serial_bus.USBdevice(vid = idVendor, pid = idProduct)
# print(dev)
# dev.close()


from universal_serial_bus import *
devices, devices_ids = find_all_devices_by_class(DEVICE_CLASS.Human_Interface_Device)
print(devices_ids)