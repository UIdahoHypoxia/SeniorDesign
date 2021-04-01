# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:44:45 2021

@author: Ironm
"""

import serial
import time
import struct

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data


loop = 1
while loop:
    num = input("Enter a number: ") # Taking input from user
    if num == 'stop':
        loop = 0
        arduino.close()
        break
    value = write_read(num)
    if value != b'':
        print(value) # printing the value
        strval = value.decode("utf-8")
        print( strval[0:3])
        if(strval[0:3] == "4.0"):
            print("woo")
        #print(type(value))
        split = value.split(b',')
        print(split)
        #for val in split:
            #print(float(val))
        #print(float(value))

