import os

# os.environ['PYUSB_DEBUG'] = 'debug'
import usb


print(usb.core.show_devices(verbose = False))
