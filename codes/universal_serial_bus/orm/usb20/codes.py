from ...orm import ModelBuilder, OrmClassBase



def map_db_objects(db_url):
    engine, meta, tables, session = ModelBuilder.get_db_objects(db_url)
    script = ModelBuilder._gen_mapping_strings(db_url, print_out = False)
    exec(script)
    return engine, meta, tables, session



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



class RequestCode(OrmClassBase):
    fields_sizes = [('rqst_code', 1), ]


    def __init__(self, request_type, rqst_code):
        self.request_type = request_type
        self.rqst_code = rqst_code
