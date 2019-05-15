from ..orm import OrmClassBase



class ClassCode(OrmClassBase):
    fields_sizes = [('base_code', 1), ]


    def __init__(self, description, descriptor_usage, base_code):
        self.description = description
        self.descriptor_usage = descriptor_usage
        self.base_code = base_code



class DescriptorType(OrmClassBase):
    fields_sizes = [('bDescriptorType', 1), ]


    def __init__(self, dscrpt_type, bDescriptorType):
        self.dscrpt_type = dscrpt_type
        self.bDescriptorType = bDescriptorType



class DeviceQualifierDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bcdUSB', 2), ('bDeviceClass', 1), ('bDeviceSubClass', 1),
                    ('bDeviceProtocol', 1), ('bMaxPacketSize0', 1), ('bNumConfigurations', 1), ('bReserved', 1), ]


    def __init__(self, bLength, bDescriptorType, bcdUSB, bDeviceClass, bDeviceSubClass, bDeviceProtocol,
                 bMaxPacketSize0, bNumConfigurations, bReserved, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bcdUSB = bcdUSB
        self.bDeviceClass = bDeviceClass
        self.bDeviceSubClass = bDeviceSubClass
        self.bDeviceProtocol = bDeviceProtocol
        self.bMaxPacketSize0 = bMaxPacketSize0
        self.bNumConfigurations = bNumConfigurations
        self.bReserved = bReserved



class OtherSpeedConfigurationDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('wTotalLength', 2), ('bNumInterfaces', 1),
                    ('bConfigurationValue', 1), ('iConfiguration', 1), ('bmAttributes', 1), ('bMaxPower', 1), ]


    def __init__(self, bLength, bDescriptorType, wTotalLength, bNumInterfaces, bConfigurationValue, iConfiguration,
                 bmAttributes, bMaxPower, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.wTotalLength = wTotalLength
        self.bNumInterfaces = bNumInterfaces
        self.bConfigurationValue = bConfigurationValue
        self.iConfiguration = iConfiguration
        self.bmAttributes = bmAttributes
        self.bMaxPower = bMaxPower



class RequestCode(OrmClassBase):
    fields_sizes = [('rqst_code', 1), ]


    def __init__(self, request_type, rqst_code):
        self.request_type = request_type
        self.rqst_code = rqst_code



class StandardConfigurationDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('wTotalLength', 2), ('bNumInterfaces', 1),
                    ('bConfigurationValue', 1), ('iConfiguration', 1), ('bmAttributes', 1), ('bMaxPower', 1), ]


    def __init__(self, bLength, bDescriptorType, wTotalLength, bNumInterfaces, bConfigurationValue, iConfiguration,
                 bmAttributes, bMaxPower, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.wTotalLength = wTotalLength
        self.bNumInterfaces = bNumInterfaces
        self.bConfigurationValue = bConfigurationValue
        self.iConfiguration = iConfiguration
        self.bmAttributes = bmAttributes
        self.bMaxPower = bMaxPower



class StandardDeviceDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bcdUSB', 2), ('bDeviceClass', 1), ('bDeviceSubClass', 1),
                    ('bDeviceProtocol', 1), ('bMaxPacketSize0', 1), ('idVendor', 2), ('idProduct', 2), ('bcdDevice', 2),
                    ('iManufacturer', 1), ('iProduct', 1), ('iSerialNumber', 1), ('bNumConfigurations', 1), ]


    def __init__(self, bLength, bDescriptorType, bcdUSB, bDeviceClass, bDeviceSubClass, bDeviceProtocol,
                 bMaxPacketSize0, idVendor, idProduct, bcdDevice, iManufacturer, iProduct, iSerialNumber,
                 bNumConfigurations, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bcdUSB = bcdUSB
        self.bDeviceClass = bDeviceClass
        self.bDeviceSubClass = bDeviceSubClass
        self.bDeviceProtocol = bDeviceProtocol
        self.bMaxPacketSize0 = bMaxPacketSize0
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.bcdDevice = bcdDevice
        self.iManufacturer = iManufacturer
        self.iProduct = iProduct
        self.iSerialNumber = iSerialNumber
        self.bNumConfigurations = bNumConfigurations



class StandardEndpointDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bEndpointAddress', 1), ('bmAttributes', 1),
                    ('wMaxPacketSize', 2), ('bInterval', 1), ]


    def __init__(self, bLength, bDescriptorType, bEndpointAddress, bmAttributes, wMaxPacketSize, bInterval,
                 parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bEndpointAddress = bEndpointAddress
        self.bmAttributes = bmAttributes
        self.wMaxPacketSize = wMaxPacketSize
        self.bInterval = bInterval



class StandardInterfaceDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bInterfaceNumber', 1), ('bAlternateSetting', 1),
                    ('bNumEndpoints', 1), ('bInterfaceClass', 1), ('bInterfaceSubClass', 1), ('bInterfaceProtocol', 1),
                    ('iInterface', 1), ]


    def __init__(self, bLength, bDescriptorType, bInterfaceNumber, bAlternateSetting, bNumEndpoints, bInterfaceClass,
                 bInterfaceSubClass, bInterfaceProtocol, iInterface, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bInterfaceNumber = bInterfaceNumber
        self.bAlternateSetting = bAlternateSetting
        self.bNumEndpoints = bNumEndpoints
        self.bInterfaceClass = bInterfaceClass
        self.bInterfaceSubClass = bInterfaceSubClass
        self.bInterfaceProtocol = bInterfaceProtocol
        self.iInterface = iInterface



class StringDescriptorZero(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('wLANGID_0_', 2), ('wLANGID_x_', 2), ]


    def __init__(self, bLength, bDescriptorType, wLANGID_0_, wLANGID_x_, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.wLANGID_0_ = wLANGID_0_
        self.wLANGID_x_ = wLANGID_x_



class UnicodeStringDescriptor(OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1), ('bString', 255), ]


    def __init__(self, bLength, bDescriptorType, bString, parent_id = None):
        self.parent_id = parent_id
        self.bLength = bLength
        self.bDescriptorType = bDescriptorType
        self.bString = bString



class UsbDevice(OrmClassBase):
    fields_sizes = []


    def __init__(self, name, description):
        self.name = name
        self.description = description
