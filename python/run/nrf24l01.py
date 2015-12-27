import RPi.GPIO as GPIO
import spidev
import wiringpi
import requests as req

def kbk(chn):
    print "KBK:"
    print radio.read_data()
    radio.flush_rx()
    radio.clear_status()

class nrf24l01:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.CE_PIN = 18
        self.IRQ_PIN = 22
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.CE_PIN, GPIO.OUT)
        GPIO.setup(self.IRQ_PIN, GPIO.IN)

   #             # if data exists
   #     if GPIO.input(self.IRQ_PIN) == 0:
   #         kbk(self.IRQ_PIN)
   #         
   #     try:
   #         GPIO.add_event_detect(self.IRQ_PIN, GPIO.FALLING, callback = kbk)
   #     except:
   #         GPIO.remove_event_detect(self.IRQ_PIN)
   #         GPIO.add_event_detect(self.IRQ_PIN, GPIO.FALLING, callback = kbk)

            
    def read_register(self, reg, length = 1):
        dumb = [0xff for x in (range(length + 1))]
        dumb.insert(0,reg)
        tmp = self.spi.xfer2(dumb);
        return tmp[1:-1]
    
    def write_register(self, reg, val):
        dumb = [0x20|reg]
        try:
            dumb = dumb + val
        except:
            dumb = dumb + [val]
            
        self.spi.xfer2(dumb)
        
    def modify_bit (self, reg, bit_pos, toval):
        #only works for 1byte reg
        origin = self.read_register(reg)[0]
        origin = origin & ~(1 << bit_pos)
        new = origin | (toval << bit_pos)
        
        self.write_register(reg, new)
        return origin
    
    def irq_callback(self,ch):
       
        self.flush_rx()
        self.clear_status()
        
        
    def read_data(self,length=0):
        dumb = [0xff for x in (range(length + 1))]
        dumb.insert(0,0b01100001)
        tmp = self.spi.xfer2(dumb);
        return tmp[1:-1]
        
    def make_rx(self):
        radio = self 
        radio.write_register(0x00,0x0B)
        radio.write_register(0x01,0x00)
        radio.write_register(0x02,0x03)
        radio.write_register(0x03,0x03)
        radio.write_register(0x04,0x03)
        radio.write_register(0x05,0x02)
        radio.write_register(0x06,0b1111)

        radio.write_register(0x09,0x00)
        radio.write_register(0x11,32)
        
        self.flip_lowhigh()
    def make_tx(self):
        radio = self
        radio.write_register(0x00,0x0A)
        radio.write_register(0x01,0x00)
        radio.write_register(0x02,0x03)
        radio.write_register(0x03,0x03)
        radio.write_register(0x04,0x03)
        radio.write_register(0x05,0x02)
        radio.write_register(0x06,0x0F)

        radio.write_register(0x08,0x00)
        radio.write_register(0x09,0x00)
        radio.write_register(0x11,0x00)
        self.flip_lowhigh()
        #tx conf
    def readall(self):
        for i in (range(0x00,0x0A) + range(0x11,0x18)):
            reg = self.read_register(i)

            print hex(i) + ":" + format(reg[0],"0b") + " | " + format(reg[0], "#04x")
    def flip_lowhigh(self):
        GPIO.output(self.CE_PIN,0)
        GPIO.output(self.CE_PIN,1)
    
    def read_data(self,length=32):
        data = self.spi.xfer([0b01100001] + [0xff for i in range (length)])
        return data[1:length]
    
    def clear_status(self):        
        self.spi.xfer([0x20|0x07, 0xff])
        
    def flush_rx(self):
        self.spi.xfer([0b11100010])
        
    def __del__(self):
        self.spi.close()
        GPIO.remove_event_detect(self.IRQ_PIN)
        
 
