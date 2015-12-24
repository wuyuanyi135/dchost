import register

class ConfigRegister (register.Register):
    Address = 0x00

    Bit_Length = 8

    Bit_Definition = [
            ("PRIM_RX", 1),
            ("PWR_UP",  1),
            ("CRCO",    1),
            ("EN_CRC",  1),
            ("MASK_MAX_RT", 1),
            ("MASK_MAX_DS", 1),
            ("MASK_RX_DR", 1),
            (None,1)
            ]

    def __init__(self):
        super(ConfigRegister,self).__init__()


