# Module to compare the two numbers and identify and error between sending via float and ASCII
import serial
import struct
ser = serial.Serial(port='COM9', baudrate=9600) 
while True:
    if(ser.inWaiting() > 2):    
        command = ser.read(1) #read the first byte
        if (command == 'm'):
            vS = ser.readline()
            #
            ser.read(1)
            data = ser.read(4)
            ser.readline()
            vF, = struct.unpack('<f',data)
            vSf = float(vS)
            diff = vF-vSf
            if (diff < 0):
                diff = 0-diff
            if (diff < 1e-11):
                diff = 0
            print(vSf)
            print(vF)
            print(diff)
            #print ("Str:", vSf, " Fl: ", vF, " Dif:", diff )