# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 11:36:09 2022

@author: Jason
"""

"""Small example OSC server

Headpat simulator, to test headpat device, sends loop of osc messages

"""

import argparse
import time

import configparser

# Config reader setup

config = configparser.ConfigParser()		
config.read("./config.ini")

# = config['OSC_RX']

#tx = config['Device_Setup']
tx_setup = config['Haptic_Config']
osc_setup = config['Setup']




# TX
from pythonosc.udp_client import SimpleUDPClient

#ip_tx = tx['Headpat_IO_IP']
ip_rx = '127.0.0.1' #osc_setup['ip_rx']
port_rx = int(osc_setup['port_rx'])  # Must be an int, config returns a str

client = SimpleUDPClient(ip_rx, port_rx)  # Create client





# OSC Setup

osc_header = '/avatar/parameters/'

#ch_1_OSC_rx = osc_setup['Channel_1_rx_Parameter']
#ch_1_OSC_rx =  osc_header + ch_1_OSC_rx 

ch_1_OSC_tx = "/avatar/parameters/proximity_01" # Hard code, arduino wont be able to change it


#max_rx = osc_setup['Headpat_Max_Parameter']
#max_rx = osc_header + max_rx 
max_rx = '/avatar/parameters/max_speed'


#https://fsymbols.com/generators/carty/
print("");
print("  ██████  ██  ██████   ██████  ██      ███████     ████████ ███████  ██████ ██   ██ ");
print(" ██       ██ ██       ██       ██      ██             ██    ██      ██      ██   ██ ");
print(" ██   ███ ██ ██   ███ ██   ███ ██      █████          ██    █████   ██      ███████ ");
print(" ██    ██ ██ ██    ██ ██    ██ ██      ██             ██    ██      ██      ██   ██ ");
print("  ██████  ██  ██████   ██████  ███████ ███████        ██    ███████  ██████ ██   ██ ");
print("");
print(" █ █ █▀█ █▀▀ █ █ ▄▀█ ▀█▀   █▀█ █▀ █▀▀   █▀ █ █▀▄▀█");
print(" ▀▄▀ █▀▄ █▄▄ █▀█ █▀█  █    █▄█ ▄█ █▄▄   ▄█ █ █ ▀ █");
print("")
print('This will emulate VRChat HeadpatIO parameters for testing')
print("")
print(f"Fowarding to Device:  {ip_rx}:{port_rx}")


def ramp_climb():
    
    for x in range(11):
        prox_send = x / 10
        print("Prox Simulation",  round(prox_send, 2))
        client.send_message(ch_1_OSC_tx, prox_send)  
        time.sleep(.01)
    for x in range(11):
        prox_send = 1 - x / 10
        print("Prox Simulation",  round(prox_send, 2))
        client.send_message(ch_1_OSC_tx, prox_send)  
        time.sleep(.05)        

def stress_test():
    client.send_message(ch_1_OSC_tx, .99)  
    time.sleep(.5)
    client.send_message(ch_1_OSC_tx, 0.0) 
    time.sleep(.5)

def ramp():
    #
    
    #input("Press Enter to Start Test...") 
    print("")
    
    ramp_climb()  
    ramp_climb()      
    ramp_climb()      

    print("Stop")    
    client.send_message(ch_1_OSC_tx, 0) 
    client.send_message(ch_1_OSC_tx, 0) 
    client.send_message(ch_1_OSC_tx, 0) 
    client.send_message(ch_1_OSC_tx, 0)  
    time.sleep(.5)

def speed_max():
    print("")
    print('Testing Max Speed Speed Parameter')
    input("Press Enter to Start Test...") 
    print("")    
    for x in range(11):
        speed_send = x / 10
        print("Speed Max Parameter:", round(speed_send,2))
        client.send_message(max_rx, speed_send)  
        time.sleep(.05)
        
        
def speed(speed):
   print("Testing Speed:", speed)
   
   client.send_message(max_rx, speed)
   time.sleep(1)
   client.send_message(ch_1_OSC_tx, 1) 
   client.send_message(ch_1_OSC_tx, 1) 
   for x in range(2):
       time.sleep(1)
   print("Stop")   
    
   client.send_message(ch_1_OSC_tx, 0) 
   client.send_message(ch_1_OSC_tx, 0) 
   client.send_message(ch_1_OSC_tx, 0) 
   client.send_message(ch_1_OSC_tx, 0)  



max_speed_test = int(tx_setup['max_speed'])

#client.send_message(max_rx, max_speed_test/100)
client.send_message(max_rx, 0.99)
import time

start_time = time.time()
count = 0
while True:

    #ramp()
    stress_test()
    count += 1
    elapsed_time = time.time() - start_time
    elapsed_minutes = int(elapsed_time / 60)
    print("This loop has run", count, "times and has been running for", elapsed_minutes, "minutes.")


speed_max()
ramp()
client.send_message(max_rx, max_speed_test/100)
print("OSC Test Complete")
print("")
input("Press Enter to Close...") 