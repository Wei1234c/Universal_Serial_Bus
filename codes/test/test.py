import universal_serial_bus


idVendor = 0x1b3f
idProduct = 0x2008

# dev = usb.core.find(idVendor = idVendor, idProduct = idProduct)
dev = universal_serial_bus.USBdevice(vid = idVendor, pid = idProduct)
print(dev)
