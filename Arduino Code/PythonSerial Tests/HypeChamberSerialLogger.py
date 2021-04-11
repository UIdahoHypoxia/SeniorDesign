import serial
import time
import csv
import datetime

#Modify the Com port to match that of the arduino

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
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

#Used to signal door open or closed to pause gasses. 
def write_StartStopPause(val):
    if(val == "Start"):
        arduino.write("Start\n".encode())
    elif(val == "Stop"):
        arduino.write("Stop\n".encode())
    elif(val == "Pause"):
        arduino.write("Pause\n".encode())
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
    arduino.write("Hello\n".encode())
    time.sleep(0.05)

def write_CSV(splitFloat, fileName):
    if(splitFloat[1] != 0):
        with open(fileName, 'a') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(splitFloat)
        writer.close()

loop = 1
pressureLimit = 1000
write_StartStopPause("Start")
while loop:
    # num = input("Enter a number: ") # Taking input from user
    # if num == 'stop':
    #     loop = 0
    #     arduino.close()
    #     break
    # write_arduino(num)
    splitFloat, data = read_ArduinoLine()
    pressure = splitFloat[5]
    
    # if(pressure >= pressureLimit*0.95):
    #     print("Pressure Warning")
    # elif(pressure >= pressureLimit):
    #     write_StartStopPause("Stop")
        
        
    #write_CSV(splitFloat, FileName)
    
    
    # if(splitFloat[1] != 0):
    #     with open(FileName, 'a') as f:
    #         writer = csv.writer(f, delimiter = ',')
    #         writer.writerow(splitFloat)

