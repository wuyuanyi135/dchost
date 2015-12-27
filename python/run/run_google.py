import requests as req
from nrf24l01 import *
import sys
radio = nrf24l01()
radio.make_rx()
radio.flush_rx()
radio.clear_status()

radio.readall()
while(1):

    if(GPIO.input(radio.IRQ_PIN))==0:
        data= radio.read_data()
        radio.flush_rx()
        radio.clear_status()
        data = data[0:4]
        
        i = data[0] | (data[1] <<8) | (data[2] <<16) | (data[3] <<24)
        
        
        thermocouple_temperature = ((i>>18) & 0x1fff)/4.0 * (-1) ** (i>>31 & 0x01)
        room_temp=((i>>4) & 0x7ff)/16.0 * (-1) ** (i>>15 & 0x01)
        
        payload = {"temp1":room_temp, "temp2":thermocouple_temperature}
        lastreq = req.get("https://script.google.com/macros/s/AKfycbzw4pMRsCS2pHyIZ_8YIDmJJmKIBy0koD3ztY0H1Gkt1duDzMQ/exec",params=payload)
