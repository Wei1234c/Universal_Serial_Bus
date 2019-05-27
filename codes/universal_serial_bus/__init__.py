import usb
import usb._interop
import usb._lookup

from orm.tools import AttrDict
from . import _lookup
from .legacy import *
from .orm import OrmClassBase



def find_all_devices_by_class(class_code):
    def find_class(class_code):
        def scan(device):
            if device.bDeviceClass == class_code:
                return True

            for cfg in device:
                for inft in cfg:
                    if inft.bInterfaceClass == class_code:
                        return True
            return False


        return scan


    devices = list(usb.core.find(find_all = True, custom_match = find_class(class_code)))
    devices_ids = sorted(set([(device.idVendor, device.idProduct) for device in devices]))
    return devices, devices_ids



class USBdevice(usb.core.Device):
    TYPE = CONTROL_REQUEST.TYPE.STANDARD
    DEFAULT_INTERFACE = (0, 0)


    def __init__(self, vid, pid, address = None, configuration = None):
        kwargs = dict(idVendor = vid, idProduct = pid)
        if address is not None:
            kwargs['address'] = address
        dev = usb.core.find(**kwargs)
        if not dev:
            raise ValueError("Device not found ({:x}:{:x} address:{})".format(vid, pid, address or ''))

        super().__init__(dev._ctx.dev, dev._ctx.backend)
        self.set_configuration(configuration)
        self.set_endpoints()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def __del__(self):
        self.close()


    @property
    def manufacturer_product(self):
        return '{} {} ( {} {} )'.format(self.manufacturer, self.product, hex(self.idVendor), hex(self.idProduct))


    @property
    def usb_version(self):
        return OrmClassBase.word_to_bcd(self.bcdUSB)


    @property
    def attributes(self):
        return self.__dict__


    @property
    def is_open(self):
        return (self._ctx.handle is not None) if hasattr(self, '_ctx') else False


    def close(self):
        if self.is_open:
            usb.util.dispose_resources(self)
            self.reset()


    def set_endpoints(self):
        config = self.get_active_configuration()
        self.endpoints = {ep.bEndpointAddress: Endpoint(ep, interface) for interface in config for ep in interface}
        pipes = {}
        for ep in self.endpoints.values():
            pipes.setdefault(ep.type, {}).setdefault(ep.direction, []).append(ep)
        self.pipes = AttrDict(pipes)


    def control_read(self, bRequest, wValue = 0, wIndex = 0, wLength = 0x400, timeout = None, type = None,
                     recipient = CONTROL_REQUEST.RECIPIENT.DEVICE):
        type = self.TYPE if type is None else type
        bmRequestType = usb.util.build_request_type(CONTROL_REQUEST.DIRECTION.IN, type, recipient)
        return self.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, wLength, timeout)


    def control_write(self, bRequest, wValue = 0, wIndex = 0, data = None, timeout = None, type = None,
                      recipient = CONTROL_REQUEST.RECIPIENT.DEVICE):
        type = self.TYPE if type is None else type
        bmRequestType = usb.util.build_request_type(CONTROL_REQUEST.DIRECTION.OUT, type, recipient)
        return self.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data, timeout)


    @classmethod
    def scan_usb_bus(cls, full = False):
        devices = list(usb.core.find(find_all = True))
        for dev in devices:
            print(dev if full else dev._str())
        return devices


    def get_descriptor(self, desc_size, desc_type, desc_index, wIndex = 0):
        return usb.control.get_descriptor(self, desc_size, desc_type, desc_index, wIndex)


    def get_string(self, index, langid = None):
        string = usb.util.get_string(self, index, langid)
        return "" if string is None else string


    def get_strings(self, lang_id = None, max = 127):
        descriptors = []

        for i in range(max):
            try:
                descriptors.append(self.get_string(i, lang_id))
            except usb.core.USBError:
                pass

        return descriptors


    @property
    def descriptors_from_config(self):
        descriptor = self.get_descriptor(DESCRIPTOR.SIZE.CONFIG, DESCRIPTOR.TYPE.CONFIG, 0)
        descriptor = self.get_descriptor(OrmClassBase.byte_array_to_int(descriptor[2:4]),
                                         DESCRIPTOR.TYPE.CONFIG, 0)
        return list(self.split_descriptor(descriptor))


    @property
    def descriptors(self):
        device_descriptor = self.get_descriptor(DESCRIPTOR.SIZE.DEVICE, DESCRIPTOR.TYPE.DEVICE, 0)
        return [device_descriptor] + self.descriptors_from_config


    def dump_descriptors(self, fn = None):
        fn = self.manufacturer_product + ' descriptors.json' if fn is None else fn
        import json

        with open(fn, 'wt') as f:
            json.dump([e.tolist() for e in self.descriptors], f)


    @classmethod
    def load_descriptors(cls, fn = None):
        fn = ' descriptors.json' if fn is None else fn
        import json
        from array import array

        with open(fn, 'rt') as f:
            return [array('B', e) for e in json.load(f)]


    @classmethod
    def split_descriptor(cls, descriptor):
        total_len = len(descriptor)
        start = 0

        while start < total_len:
            seg_len = descriptor[start]
            assert seg_len > 0, 'Descriptor length is 0.'
            yield descriptor[start: start + seg_len]
            start = start + seg_len


    @property
    def descriptors_dbos(self):
        return self.get_descriptors_dbos(self.descriptors)


    @classmethod
    def load_descriptors_dbos(cls, fn = None):
        descriptors = cls.load_descriptors(fn)
        return cls.get_descriptors_dbos(descriptors)


    @classmethod
    def get_descriptors_dbos(cls, descriptors):
        dbos = []
        intf_type = None

        for descriptor in descriptors:
            _class, intf_type = cls._categorize(descriptor, intf_type)

            if _class is not None:
                dbos.append(_class.from_byte_array(descriptor))

        return dbos


    @property
    def device_descriptor_dbo(self):
        return self.descriptors_dbos[0]


    @property
    def configuration_descriptor_dbo(self):
        return self.descriptors_dbos[1]



class Endpoint(usb.core.Endpoint):

    def __init__(self, endpoint, interface):
        self.device = endpoint.device
        self.interface = interface
        self.index = endpoint.index

        usb.core._set_attr(endpoint, self, ('bLength', 'bDescriptorType', 'bEndpointAddress',
                                            'bmAttributes', 'wMaxPacketSize', 'bInterval', 'bRefresh',
                                            'bSynchAddress', 'extra_descriptors'))


    def set_interface(self):
        try:
            self.device.set_interface_altsetting(self.interface)
        except usb.core.USBError as e:
            print(e)


    @property
    def direction(self):
        direction = usb.util.endpoint_direction(self.bEndpointAddress)
        return _lookup.endpoint_direction[direction]


    @property
    def type(self):
        return usb._lookup.ep_attributes[(self.bmAttributes & ENDPOINT.TYPE.MASK)]


    @property
    def type_direction(self):
        return self._str()
