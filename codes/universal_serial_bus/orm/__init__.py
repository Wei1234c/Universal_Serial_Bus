import math
from array import array

import orm.alchemy



class OrmClassBase(orm.alchemy.OrmClassBase):
    fields_sizes = (('bLength', 1), ('bDescriptorType', 1))
    BYTEORDER = 'little'


    @classmethod
    def int_to_byte_array(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        length = math.ceil(math.log2(value + 1) / 8) if length is None else length
        length = max(length, 1)
        return array('B', value.to_bytes(length, byteorder, signed = signed))


    @classmethod
    def int_to_hex(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        byte_array = cls.int_to_byte_array(value, length, byteorder, signed)
        return cls.byte_array_to_hex(byte_array)


    @classmethod
    def bcd_to_hex(cls, bcd):
        major = '{:0>2}'.format(int(bcd // 1))
        minor = '{:0<2}'.format(int((bcd % 1) * 100))
        return minor + major


    @classmethod
    def hex_to_bcd(cls, hex_string):
        major = int(hex_string[2:4])
        minor = int(hex_string[0:2]) / 100
        return major + minor


    @classmethod
    def int_eq_hex(cls, i, hex_string, length = None, byteorder = BYTEORDER, signed = False):
        return cls.int_to_hex(i, length, byteorder, signed) == hex_string.lower()


    @classmethod
    def byte_array_to_int(cls, byte_array, byteorder = BYTEORDER, signed = False):
        return int.from_bytes(byte_array.tobytes(), byteorder = byteorder, signed = signed)


    @classmethod
    def hex_to_int(cls, hex_string, byteorder = BYTEORDER, signed = False):
        return int.from_bytes(bytes.fromhex(hex_string), byteorder = byteorder, signed = signed)


    @classmethod
    def byte_array_to_hex(cls, byte_array):
        return byte_array.tobytes().hex()


    @classmethod
    def bytes_to_hex(cls, value_bytes):
        return value_bytes.hex()


    @classmethod
    def hex_to_byte_array(cls, hex_string):
        return array('B', bytes.fromhex(hex_string))


    @classmethod
    def hex_reversed(cls, hex_string):
        byte_array = cls.hex_to_byte_array(hex_string)
        byte_array.reverse()
        return cls.byte_array_to_hex(byte_array)


    @classmethod
    def from_byte_array(cls, byte_array, parent_id = None):
        return cls(*(cls.get_descriptor_fields_values(byte_array)), parent_id = parent_id)


    @classmethod
    def from_zeros(cls, parent_id = None):
        fields_values = [cls.byte_array_to_hex(array('B', [0] * cls.fields_sizes[i][1]))
                         for i in range(len(cls.fields_sizes))]
        return cls(*(fields_values), parent_id = parent_id)


    @property
    def byte_array(self):
        b_array = array('B', [])
        for i in range(len(self.fields_sizes)):
            b_array += self.hex_to_byte_array(getattr(self, self.fields_sizes[i][0]))
        return b_array


    @classmethod
    def concate_byte_arrays(cls, dbos):
        byte_array = array('B', [])
        for dbo in dbos:
            byte_array += dbo.byte_array
        return byte_array


    @classmethod
    def get_descriptor_fields_values(cls, descriptor_array, to_hex = True):
        fields_values = []
        start = 0

        for i in range(len(cls.fields_sizes)):
            size = cls.fields_sizes[i][1]
            value = descriptor_array[start: start + size]
            fields_values.append(cls.byte_array_to_hex(value) if to_hex else value)
            start += size

        return fields_values


    @classmethod
    def split_descriptor(cls, descriptor):
        total_len = len(descriptor)
        start = 0

        while start < total_len:
            seg_len = descriptor[start]
            assert seg_len > 0, 'Descriptor length is 0.'
            yield descriptor[start: start + seg_len]
            start = start + seg_len



class ModelBuilder(orm.alchemy.ModelBuilder):

    @classmethod
    def _gen_imports(cls):
        # print('from universal_serial_bus.orm import OrmClassBase')
        super()._gen_imports()


    @classmethod
    def _gen_class_header(cls, table):
        class_name = cls._class_name_from_table_name(table.name)
        return 'class {}(OrmClassBase):\n'.format(class_name)


    @classmethod
    def _gen_class_variables(cls, table):
        fields = ["('{}', {}),".format(column.name, column.type.length // 2)
                  for column in table.columns
                  if ((not column.primary_key)
                      and hasattr(column.type, 'length')
                      and isinstance(column.type.length, int))]
        variable = cls.INDENT + 'fields_sizes = [{}]'.format(' '.join(fields))
        return [variable, '']


    @classmethod
    def _gen_fields_declaration(cls, table):
        fields = [column.name for column in table.columns if not column.primary_key]
        parent_at_1st = fields[0] == 'parent_id'
        if parent_at_1st:
            fields_declaration = ', '.join(fields[1:] + [fields[0]]) + " = None"
        else:
            fields_declaration = ', '.join(fields)
        return cls.INDENT + 'def __init__(self, {}):\n'.format(fields_declaration)
