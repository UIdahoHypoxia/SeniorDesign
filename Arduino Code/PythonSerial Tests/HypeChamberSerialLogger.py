


import serial
import time
import csv


arduino = serial.Serial(port='COM9', baudrate=115200, timeout=.1)
splitFloat = [0,0]
fieldnames = ['Time', 'O2', 'CO2', 'Temperature', 'Humidty', 'Pressure', 'O2Solenoid', 'CO2Solenoid']
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
        #print(type(value))
        split = value.split(b',')
        #print(split)
        for i in range(len(split)):
            splitFloat[i] = float(split[i])
        with open('some.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(splitFloat)
        #print(float(value))

