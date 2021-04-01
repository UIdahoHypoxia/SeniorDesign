import serial
import time
import csv
import datetime

#Modify the Com port to match that of the arduino
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
#The base declartion of the array for values to be stored into
#Time, O2, CO2, Temp, Humidity, Pressure, O2Solenoid Time, CO2Solenoid Time
splitFloat = [0,0,0,0,0,0,0,0]
#Used to clear and reset splitFloat after each reading
splitFloatZeros = [0,0,0,0,0,0,0,0]

#The CSV file to save into, eventually changed via the interface
FileName = 'some.csv'

#Sets the O2 setpoint
def write_O2(O2):
    O2 = "O2 " + O2
    O2 = bytes(O2, 'utf-8')
    arduino.write(O2)
    time.sleep(0.02)

#Sets the CO2 Setpoint
def write_CO2(CO2):
    CO2 = "CO2 " + CO2
    CO2 = bytes(CO2, 'utf-8')
    arduino.write(CO2)
    time.sleep(0.02)   

#Used to signal door open or closed to pause gasses. Val = 1 Pause, Val = 0 Run
def write_Door(val):
    val = "Door " + val
    val = bytes(val, 'utf-8')
    arduino.write(val)
    time.sleep(0.02)

def read_ArduinoLine():
    splitFloat = [0,0,0,0,0,0,0,0]
    data = arduino.readline()
    if data != b'':
        print(data)
        strData = data.decode("utf-8")
        if(strData[0:2] == "V:"):
            split = strData[2:].split(",")
            splitFloat[0] = datetime.datetime.now()
            for i in range(len(split)):
                splitFloat[i+1] = float(split[i])
            print(splitFloat)
        
    return splitFloat, data
    

def write_arduino(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)


loop = 1
while loop:
    # num = input("Enter a number: ") # Taking input from user
    # if num == 'stop':
    #     loop = 0
    #     arduino.close()
    #     break
    #write_arduino(num)
    splitFloat, data = read_ArduinoLine()
    # if value != b'':
    #     print(value) # printing the value
    #     #print(type(value))
    #     split = value.split(b',')
    #     #print(split)
    #     splitFloat = splitFloatZeros
    #     splitFloat[0] = datetime.datetime.now()
    #     for i in range(len(split)):
    #         splitFloat[i+1] = float(split[i])
    if(splitFloat[1] != 0):
        with open(FileName, 'a') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(splitFloat)

