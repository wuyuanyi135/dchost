import requests as req
from nrf24l01 import *
import sys
from prettytable import PrettyTable
radio = nrf24l01()
radio.make_rx()
radio.flush_rx()
radio.clear_status()

radio.readall()
while(1):

    if(GPIO.input(radio.IRQ_PIN))==0:
        recv_data= radio.read_data()
        radio.flush_rx()
        radio.clear_status()
        
        tab_buf = []
        tab_obj = PrettyTable(["TC#","TC","RT","ER"])

        for index in range (4):
            tab_buf = []
            data = recv_data[0+index*4:4+index*4]
        
            i = data[0] | (data[1] <<8) | (data[2] <<16) | (data[3] <<24)
        
            error_code = i & 0b111
            
            error_buf = []

            if error_code & 0b001 != 0:
                error_buf.append("NO CONNECT")
            if error_code & 0b010 != 0:
                error_buf.append("SHORT GND")
            if error_code & 0b100 != 0:
                error_buf.append("SHORT VCC")

            error_msg = "|".join(error_buf)

            thermocouple_temperature = ((i>>18) & 0x1fff)/4.0 * (-1) ** (i>>31 & 0x01)
            room_temp=((i>>4) & 0x7ff)/16.0 * (-1) ** (i>>15 & 0x01)

            #tab_buf.append([thermocouple_temperature, room_temp, error_msg])
            tab_obj.add_row([str(index), str(thermocouple_temperature), str(room_temp), error_msg])

        print tab_obj

        

       
