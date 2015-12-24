from collections import OrderedDict

class Register (object):
    
    Address = None
    Bit_Length = None
    LittleEndian = False
    Left_MSB = True

    """
    For example, bit definition is in this format
    [ ("bits name", Length, callback(value))]
    where callback is optional
    For reversed bits, use None as its name. They will be skipped
    """

    Bit_Definition = []

    def __init__ (self, value = None ):
        self.value = value
        
        self.bits_dict = OrderedDict() 
        for bits in self.Bit_Definition:
            bits_name = bits[0]
            if bits_name is None :
                continue
            self.bits_dict[bits_name] = 0


    def decode(self):
        #TODO: check length
 
        value = self.value
        
        if self.LittleEndian == True:
            value = self.endian_adapt(value)    
            

        if self.Left_MSB == False:
            value = self.MSB_adapt(value) 

        offset = 0
        for bits in self.Bit_Definition:
            bits_name = bits[0]
            if bits_name is None:
                continue

            bits_Length = bits[1]
             
                   
            try:
                bits_value = self.read_offset(value,offset, bits_Length)
            except Exception as e: 
                raise Exception ("Length mismatch!" + str(e))
            
            # if call back funciton is present
            try:
                callback = bits[2]
                bits_value = callback(bits_value)
            except:
                pass

            offset += bits_Length
             
            self.bits_dict[bits_name] = bits_value
        return self.bits_dict

    def encode(self, package=None):
        if package is None:
            package = self.bits_dict

        built = 0 
        for index, bits in reversed(list(enumerate(self.Bit_Definition))):
            bits_name = bits[0]
            
            item = None
            if bits_name is None:
                item = 0
            else: 
                try:
                    item = package[bits_name]
                except:
                    raise Exception("Register missing!:"+bits_name)

            length = bits[1]
            built <<= length
            built = built | (item & (2 ** length - 1 ))

        return built

    @classmethod
    def read_offset(cls, value, offset, length):
        result = 0

        op_num = value >>  offset

        mask = 2 ** length - 1
        
        result = op_num & mask

        return result


    @classmethod
    def endian_adapt (cls, value):
        raise NotImplementedError()
   
    @classmethod
    def MSB_adapt (cls, value):
        raise NotImplementedError()
