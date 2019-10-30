from array import array

import orm.alchemy
from orm.tools import AttrDict



class OrmClassBase(orm.alchemy.OrmClassBase):
    fields_sizes = [('bLength', 1), ('bDescriptorType', 1)]
    BYTEORDER = 'little'


    @property
    def attributes(self):
        return {field_size[0]: getattr(self, field_size[0]) for field_size in self.fields_sizes}


    def find_field_size(self, field_name):
        for idx in range(len(self.fields_sizes)):
            if self.fields_sizes[idx][0] == field_name:
                return idx, self.fields_sizes[idx]
        return None, None


    def get_size_of_field(self, field_name):
        idx, field_size = self.find_field_size(field_name)
        if field_size is not None:
            return field_size[1]


    def delattr(self, attr_name):
        idx, field_size = self.find_field_size(attr_name)
        if idx is not None:
            self.fields_sizes.pop(idx)
            delattr(self, attr_name)


    def setattr(self, attr_name, attr_value, size = None, idx = None):
        self.delattr(attr_name)
        size = len(self.hex_to_byte_array(attr_value)) if size is None else size
        attr_names = [field_size[0] for field_size in self.fields_sizes]

        if attr_name not in attr_names:
            if idx is None:
                self.fields_sizes.append((attr_name, size))
            else:
                self.fields_sizes.insert(idx, (attr_name, size))
        setattr(self, attr_name, attr_value)


    def set_attr_hex_value_from_int(self, attr_name, value, byteorder = BYTEORDER, signed = False):
        setattr(self, attr_name,
                self.int_to_hex(value = value,
                                length = self.get_size_of_field(attr_name),
                                byteorder = byteorder,
                                signed = signed))


    @classmethod
    def int_to_byte_array(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        max_int_bytes = 8  # sys.maxsize = 9223372036854775807 < 2**(8*8)
        lengths = (1, max_int_bytes + 1) if length is None else (length, length + 1)

        for l in range(*lengths):
            try:
                return array('B', value.to_bytes(l, byteorder, signed = signed))
            except OverflowError as e:
                if length is not None:
                    raise e


    @classmethod
    def float_to_byte_array(cls, value, int_bytes = 1, decimal_bytes = 1, byteorder = BYTEORDER, signed = False):
        integer = cls.int_to_byte_array(int(value), length = int_bytes, byteorder = byteorder, signed = signed)
        decimal = int((value - int(value)) * 2 ** (decimal_bytes * 8))
        decimal = cls.int_to_byte_array(abs(decimal), length = decimal_bytes, byteorder = byteorder, signed = False)
        return decimal + integer if byteorder == cls.BYTEORDER else integer + decimal


    @classmethod
    def byte_array_to_float(cls, byte_array, int_bytes = 1, byteorder = BYTEORDER, signed = False):
        decimal_bytes = len(byte_array) - int_bytes

        if byteorder == cls.BYTEORDER:
            integer, decimal = byte_array[decimal_bytes:], byte_array[:decimal_bytes]
        else:
            integer, decimal = byte_array[:int_bytes], byte_array[int_bytes:]

        integer = cls.byte_array_to_int(integer, byteorder = byteorder, signed = signed)
        decimal = cls.byte_array_to_int(decimal, byteorder = byteorder, signed = False)
        decimal /= 2 ** (8 * decimal_bytes)
        return integer + decimal


    @classmethod
    def int_to_hex(cls, value, length = None, byteorder = BYTEORDER, signed = False):
        byte_array = cls.int_to_byte_array(value, length, byteorder, signed)
        return cls.byte_array_to_hex(byte_array)


    @classmethod
    def bcd_to_hex(cls, bcd):
        return ''.join([str(int(bcd * d))[-1] for d in (10, 100, 1 / 10, 1)])


    @classmethod
    def hex_to_bcd(cls, hex_string):
        return int(''.join(hex_string[i] for i in (2, 3, 0, 1))) / 100


    @classmethod
    def word_to_bcd(cls, word, byteorder = 'big'):
        return int(word.to_bytes(2, byteorder = byteorder).hex()) / 100


    @classmethod
    def byte_array_to_bcd(cls, byte_array, byteorder = 'little'):
        if byteorder != 'little':
            byte_array.reverse()
        return OrmClassBase.hex_to_bcd(byte_array.tobytes().hex())


    @classmethod
    def int_eq_hex(cls, i, hex_string, length = None, byteorder = BYTEORDER, signed = False):
        return cls.int_to_hex(i, length, byteorder, signed).lower() == hex_string.lower()


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
    def byte_array_to_hex_array(cls, byte_array):
        return [hex(b) for b in byte_array]


    @classmethod
    def bytes_to_hex(cls, value_bytes):
        return value_bytes.hex()


    @classmethod
    def string_to_hex_array(cls, string, hex_prefix = True, encoding = 'utf-16-le'):
        prefix = '0x' if hex_prefix else ''
        bs = string.encode(encoding = encoding)
        return [prefix + '{:02X}'.format(b) for b in bs]


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
        fields_values = [cls.byte_array_to_hex(array('B', [0] * field_size[1])) for field_size in cls.fields_sizes]
        return cls(*(fields_values), parent_id = parent_id)


    @property
    def byte_array(self):
        b_array = array('B', [])
        for i in range(len(self.fields_sizes)):
            b_array += self.hex_to_byte_array(getattr(self, self.fields_sizes[i][0]))
        return b_array


    @property
    def length(self):
        return len(self.byte_array)


    @classmethod
    def size(cls):
        return sum([field_size[1] for field_size in cls.fields_sizes])


    @classmethod
    def concate_byte_arrays(cls, dbos):
        byte_array = array('B', [])
        for dbo in dbos:
            byte_array += dbo.byte_array
        return byte_array


    @classmethod
    def total_length(cls, dbos):
        return len(cls.concate_byte_arrays(dbos))


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
    def gen_constants(cls, key_field, value_field, session, as_hex = True):
        d = cls.to_dict([key_field], [value_field], session)
        return AttrDict({k[0]: int('0x' + v[0], 16) if as_hex else int(v[0]) for k, v in d.items()})



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
