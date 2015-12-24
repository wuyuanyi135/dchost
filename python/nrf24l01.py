"""

Dependency: spidev; RPi.GPIO; 

"""

import spidev

class NRF24L01:

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        if value > 2 :
            raise Exception("Client number mismatch")
        self._client = value

    @property
    def bus(self):
        return self._bus
    @property.setter
    def bus(self,value):
        if value > 2:
            raise Exception("Bus number mismatch")
        self._bus = bus
   
    def __init__(self, bus, client):

        # spidev instance 
        self.spi = spidev.SpiDev()
        
        self.bus = bus

        self.client = client
        
        self.spi_opened = False
   """
    
    open the spi port 
    """
    def open(self, bus = None, client = None):
        _bus = self.bus
        _client = self.client

        if bus != None:
           _bus = bus

        if client != None:
            _client = client

        try:
            self.spi.open(_bus,_client)
        except (e):
            raise Exception ( "failed to open the spi port: " + str(e) )
        self.spi_opened = True



    """
    close the port
    """
    def close (self):
        if not self.spi_opened :
            raise Exception("Spi port has not been opened")

        self.spi.close()

        

        
