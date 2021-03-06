ERROR_BEGIN = 500000
MAX_ALT_SETTING = 128
MAX_CONFIG = 8
MAX_ENDPOINTS = 32
MAX_INTERFACES = 32



class DEVICE_CLASS:
    Use_class_information_in_the_Interface_Descriptors = 0x00
    Audio = 0x01
    Communications_and_CDC_Control = 0x02
    Human_Interface_Device = 0x03
    Physical = 0x05
    Image = 0x06
    Printer = 0x07
    Mass_Storage = 0x08
    Hub = 0x09
    CDC_Data = 0x0A
    Smart_Card = 0x0B
    Content_Security = 0x0D
    Video = 0x0E
    Personal_Healthcare = 0x0F
    Audio_Video_Devices = 0x10
    Billboard_Device_Class = 0x11
    USB_Type_C_Bridge_Class = 0x12
    Diagnostic_Device = 0xDC
    Wireless_Controller = 0xE0
    Miscellaneous = 0xEF
    Application_Specific = 0xFE
    Vendor_Specific = 0xFF



class DESCRIPTOR:
    class TYPE:
        DEVICE = 0x01
        CONFIG = 0x02
        STRING = 0x03
        INTERFACE = 0x04
        ENDPOINT = 0x05
        QUALIFIER = 0x06
        INTERFACE_ASSOCIATION = 0x0B
        HID = 0x21
        REPORT = 0x22
        PHYSICAL = 0x23
        HUB = 0x29


    class SIZE:
        DEVICE = 18
        QUALIFIER = 10
        CONFIG = 9
        INTERFACE = 9
        INTERFACE_ASSOCIATION = 8
        ENDPOINT = 7
        ENDPOINT_AUDIO = 9
        HUB_NONVAR = 7



class ENDPOINT:
    ADDRESS_MASK = 0x0F


    class DIRECTION:
        MASK = 0x80
        IN = 0x80
        OUT = 0x00


    class TRANSFER_TYPE:
        MASK = 0x03
        CONTROL = 0x00
        ISOCHRONOUS = 0x01
        BULK = 0x02
        INTERRUPT = 0x03


    class SYNCHRONIZATION_TYPE:
        MASK = 0x0C
        NO_SYNCHRONIZATION = 0x00
        ASYNCHRONOUS = 0x01
        ADAPTIVE = 0x02
        SYNCHRONOUS = 0x03


    class USAGE_TYPE:
        MASK = 0x30
        DATA_ENDPOINT = 0x00
        FEEDBACK_ENDPOINT = 0x01
        IMPLICIT_FEEDBACK_DATA_ENDPOINT = 0x02
        RESERVED = 0x03



class CONTROL_REQUEST:
    MASK = 0x0F
    GET_STATUS = 0x00
    CLEAR_FEATURE = 0x01
    SET_FEATURE = 0x03
    SET_ADDRESS = 0x05
    GET_DESCRIPTOR = 0x06
    SET_DESCRIPTOR = 0x07
    GET_CONFIGURATION = 0x08
    SET_CONFIGURATION = 0x09
    GET_INTERFACE = 0x0A
    SET_INTERFACE = 0x0B
    SYNCH_FRAME = 0x0C


    class DIRECTION:
        MASK = 0x80
        OUT = 0x00
        IN = 0x80


    class TYPE:
        MASK = 0x60
        STANDARD = 0x00
        CLASS = 0x20
        VENDOR = 0x40
        RESERVED = 0x60


    class RECIPIENT:
        MASK = 0x03
        DEVICE = 0x00
        INTERFACE = 0x01
        ENDPOINT = 0x02
        OTHER = 0x03



class SPEED_TYPE:
    MASK = 0x07
    LOW = 0x01
    FULL = 0x02
    HIGH = 0x03
    SUPER = 0x04
    UNKNOWN = 0x00
