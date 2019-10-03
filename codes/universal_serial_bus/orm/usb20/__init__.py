import universal_serial_bus
from .descriptors import *


int_eq_hex = OrmClassBase.int_eq_hex
int_to_hex = OrmClassBase.int_to_hex



class USBdevice(universal_serial_bus.USBdevice):

    @classmethod
    def _categorize(cls, descriptor, intf_type = None):

        _class = None

        if int_eq_hex(descriptor[1], '01'):  # 如果是 device
            _class = StandardDeviceDescriptor

        if int_eq_hex(descriptor[1], '02'):  # 如果是 config
            _class = StandardConfigurationDescriptor

        if int_eq_hex(descriptor[1], '05'):  # 如果是 endpoint
            _class = StandardEndpointDescriptor

        if int_eq_hex(descriptor[1], '04'):  # 如果是 interface
            _class = StandardInterfaceDescriptor

        if int_eq_hex(descriptor[1], '03'):  # 如果是 interface
            _class = UnicodeStringDescriptor

        return _class, intf_type
