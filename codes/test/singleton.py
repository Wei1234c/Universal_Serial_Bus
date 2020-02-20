class T:
    _singleton = None


    @classmethod
    def __new__(cls, *arg, **kwargs):
        if cls._singleton is None:
            cls._singleton = object.__new__(cls)

        return cls._singleton


    def __init__(self, lib = None):
        if lib:
            self.lib = lib



t1 = T(1)
t2 = T()
print(t1 is t2)
print(t2.lib)
