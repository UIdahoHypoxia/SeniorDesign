# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:14:04 2021
@authors: Izzie Strawn, Colin Marchus, Jacob Knudson, Andrew Hartman, Alex Morrison

Notes:
    *This program is for the GUI of a custom hypoxia chamber setup
    *The 'Set Values' button needs to be pressed twice the first time for some reason.
"""

## import modules
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import serial
import serial.tools.list_ports
import time
import csv
import datetime
import shutil

#Default Values for filling in the entries with Grey text
O2_Preload = 5
CO2_Preload= 5
Pres_Preload = 940
filename_Preload = "Filename Suffix"
filePath_Preload = "D:/.../MMDDYY_HHMM_FilenameSuffix.csv"
Time_Preload = 10
KpO2_Preload = 200
KiO2_Preload = 5
KpCO2_Preload = 140
KiCO2_Preload = 5

#The file path for the settings csv file.
#settings_Path = "/home/pi/HYPOXIA/settings.csv"
settings_Path =  "./settings.csv"

#Read the values from settings.csv and store it into the appropriate global variables
def read_Settings(eff=None, o2_entry=None, co2_entry=None, press_entry=None):
    global O2_Preload
    global CO2_Preload
    global Pres_Preload
    global filename_Preload
    global filePath_Preload
    global  Time_Preload
    global  KpO2_Preload
    global KiO2_Preload
    global KpCO2_Preload
    global KiCO2_Preload
    with open(settings_Path, 'r') as f:
        reader = csv.reader(f)
        settings = next(reader)
    
    O2_Preload = settings[0]
    CO2_Preload= settings[1]
    Pres_Preload = settings[2]
    if(o2_entry != None):
        o2_entry.delete(0,"end")
        o2_entry.insert(0,str(O2_Preload))
        co2_entry.delete(0,"end")
        co2_entry.insert(0,CO2_Preload)
        press_entry.delete(0,"end")
        press_entry.insert(0,Pres_Preload)
    #filename_Preload = settings[3]
    #filePath_Preload = settings[4]
    Time_Preload = settings[5]
    KpO2_Preload = settings[6]
    KiO2_Preload = settings[7]
    KpCO2_Preload = settings[8]
    KiCO2_Preload = settings[9]
    set_preloads()
    
#Save the current settings to the CSV for future reads
def write_Settings():
    global O2_Preload
    global CO2_Preload
    global Pres_Preload
    global filename_Preload
    global filePath_Preload
    global  Time_Preload
    global  KpO2_Preload
    global KiO2_Preload
    global KpCO2_Preload
    global KiCO2_Preload
    settings = [o2_entry.get(), co2_entry.get(),press_entry.get(),file_name_entry.get(), path_entry.get(), Time_Preload, KpO2_Preload, KiO2_Preload, KpCO2_Preload,KiCO2_Preload]
    with open(settings_Path, 'w') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerow(settings)


def set_preloads():
    global O2_Preload
    global CO2_Preload
    global Pres_Preload
    global filename_Preload
    global filePath_Preload
    global  Time_Preload
    global  KpO2_Preload
    global KiO2_Preload
    global KpCO2_Preload
    global KiCO2_Preload
    if(arduinoConnected == True):
        write_O2(O2_Preload)
        write_CO2(CO2_Preload)
        write_arduino("time " + Time_Preload)
        write_arduino("KpO2 " + KpO2_Preload)
        write_arduino("KiO2 " + KiO2_Preload)
        write_arduino("KpCO2 " + KpCO2_Preload)
        write_arduino("KiCO2 " + KiCO2_Preload)
    

#Write the passed in O2 value to the Arduino to set the O2 setpoint
def write_O2(O2):
    O2 = "O2 " + str(O2) + "\n"
    O2 = O2.encode()
    arduino.write(O2)
    time.sleep(0.02)

#Sets the CO2 Setpoint
def write_CO2(CO2):
    CO2 = "CO2 " + str(CO2) + "\n"
    CO2 = CO2.encode()
    arduino.write(CO2)
    time.sleep(0.02)   

#Used to signal door open or closed to pause gasses. val = "Start" will start the arduino, sensing and Solenoid control, "Stop" will stop the arduino sensing and solenoid control, "Pause" will toggle solenoid control but will keep sensing and coms running
def write_StartStopPause(val):
    if(val == "Start"):
        arduino.write("Start\n".encode())
    elif(val == "Stop"):
        arduino.write("Stop\n".encode())
    elif(val == "Pause"):
        arduino.write("Pause\n".encode())
    time.sleep(0.02)

#Reads the data coming from the Arduino over serial and splits it into a list
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
    
#writes whatever is passed in directly to the arduino
def write_arduino(x):
    arduino.write(x.encode())
    time.sleep(0.05)
 
#Stores the data passed into splitFloat as a list into the passed in filename
def write_CSV(splitFloat, fName):
    if(splitFloat[1] != 0):
        with open(fName, 'a',newline='') as f:
            writer = csv.writer(f, delimiter = ',')
            writer.writerow(splitFloat)
     
#copies the file from src to dst, dst is a directory path and the file keeps the name it had at source
def export_to_USB(src,dst):
    shutil.copy(src,dst)

#Checks if this is the first time a cell is clicked and gets rid of the grey text preloaded into it        
def on_entry_click(eff=None, entry=None):
    """function that gets called whenever entry is clicked"""
    if entry != None:
        if entry.cget('fg') == 'grey':
           entry.delete(0, "end") # delete all the text in the entry
           entry.insert(0, '') #Insert blank for user input
           entry.config(fg = 'black')
           
#If new text was not written into the cell it goes back to the preloaded filler
def on_focusout(eff = None, entry = None, PreLoad = 'Filler'):
    if entry != None:
        if len(entry.get()) - entry.get().count(' ') < 1 :
            entry.insert(0, PreLoad)
            entry.config(fg = 'grey')
            
#Preloads the defined text into the passed in entry and assignes them to the on entry click and on focusout functions
def preload_Text(entry = None, Preload = "Not Defined"):
    if(entry != None):
        entry.insert(0, Preload)
        entry.bind('<FocusIn>', lambda eff: on_entry_click(eff, entry))
        entry.bind('<FocusOut>', lambda eff: on_focusout(eff, entry, Preload))
        entry.config(fg = 'grey')

#Creates the PID Settings window
def create_window():
    upperWindow = tk.Toplevel(window)
    upperWindow.title("Hypoxia Chamber Settings GUI")
    upperWindow.configure(bg='gold')
   
    intro_frame = tk.Frame(master = upperWindow)
    intro_frame.configure(bg='gold')
    intro_label = tk.Label(master = intro_frame, text = "Control Settings", font=("Arial",15), bg=("gold"))
    intro_label_2 = tk.Label(master = intro_frame, text = "Must be set before beginning experiment", font=("Arial",10), bg=("gold"))
    intro_label.grid() 
    intro_label_2.grid()
   
    settingsWindow_frame = tk.Frame(master = upperWindow, relief = 'ridge', borderwidth = 5, bg = "black")
    
    # all of the labels and Entries go here ****************
    
    #create a textbox where the time to wait between measurements can be input
    measure_label = tk.Label(master = settingsWindow_frame, text = "Measurement Interval (s)", fg="gold",bg="black")
    measure_entry = tk.Entry(master = settingsWindow_frame)
    preload_Text(measure_entry, Time_Preload)

    
    measure_label.grid(row=0, column=0)
    measure_entry.grid(row=0, column = 1, padx=5, pady=5) 
    
    #O2 PID values
    #create a textbox where the Kp for O2 can be set
    KpO2_label = tk.Label(master = settingsWindow_frame, text = "Kp for O2", fg="gold",bg="black")
    KpO2_entry = tk.Entry(master = settingsWindow_frame)
    preload_Text(KpO2_entry, KpO2_Preload)
    
    KpO2_label.grid(row=1, column=0)
    KpO2_entry.grid(row=1, column = 1, padx=5, pady=5) 
    
    #create a textbox where the Ki for O2 can be set
    KiO2_label = tk.Label(master = settingsWindow_frame, text = "Ki for O2", fg="gold",bg="black")
    KiO2_entry = tk.Entry(master = settingsWindow_frame)
    preload_Text(KiO2_entry, KiO2_Preload)
    
    KiO2_label.grid(row=2, column=0)
    KiO2_entry.grid(row=2, column = 1, padx=5, pady=5) 
    
    #CO2 PID values    
    #create a textbox where the Kp for O2 can be set
    KpCO2_label = tk.Label(master = settingsWindow_frame, text = "Kp for CO2", fg="gold",bg="black")
    KpCO2_entry = tk.Entry(master = settingsWindow_frame)
    preload_Text(KpCO2_entry, KpCO2_Preload)
    
    KpCO2_label.grid(row=3, column=0)
    KpCO2_entry.grid(row=3, column = 1, padx=5, pady=5) 
  
    
    #create a textbox where the Ki for O2 can be set
    KiCO2_label = tk.Label(master = settingsWindow_frame, text = "Ki for CO2", fg="gold",bg="black")
    KiCO2_entry = tk.Entry(master = settingsWindow_frame)
    preload_Text(KiCO2_entry, KiCO2_Preload)
    
    KiCO2_label.grid(row=4, column=0)
    KiCO2_entry.grid(row=4, column = 1, padx=5, pady=5)
    
    def set_Values():
        measureTime = measure_entry.get() #assigns the input target o2 percentage to a variable
        KpO2 = KpO2_entry.get()
        KiO2 = KiO2_entry.get()
        KpCO2 = KpCO2_entry.get()
        KiCO2 = KiCO2_entry.get()
        print(measureTime)
        print(KpO2)
        print(KiO2)
        print(KpCO2)
        print(KiCO2)
        
        global Time_Preload
        global KpO2_Preload
        global KiO2_Preload
        global KpCO2_Preload
        global KiCO2_Preload
    
        Time_Preload = measureTime
        KpO2_Preload = KpO2
        KiO2_Preload = KiO2
        KpCO2_Preload = KpCO2
        KiCO2_Preload = KiCO2
        
        write_arduino("time " + measureTime)
        write_arduino("KpO2 " + KpO2)
        write_arduino("KiO2 " + KiO2)
        write_arduino("KpCO2 " + KpCO2)
        write_arduino("KiCO2 " + KiCO2)
        
        setValues_label['text'] = ("Values Saved")
        measure_entry.config(fg = 'black')
        KpO2_entry.config(fg = 'black')
        KiO2_entry.config(fg = 'black')
        KpCO2_entry.config(fg = 'black')
        KiCO2_entry.config(fg = 'black')
    
    #End of Set Values
    setValues_label = tk.Label(master = settingsWindow_frame, text = "", fg = "gold", bg = "black")
    setValues_label.grid(row = 5, column = 0)
    
    setvalues_button = tk.Button(master = settingsWindow_frame, text="Set values", background = ('silver'), width = 15, height = 1, relief = "ridge", borderwidth = 5, fg="black", command = set_Values)
    setvalues_button.grid(row = 5, column = 1)
    
    
    #Organize the frames of the settings window
    intro_frame.grid(row = 0, column = 0)
    settingsWindow_frame.columnconfigure([0,1,2,3,4,5,6], weight = 1 )
    settingsWindow_frame.grid(row = 1, column =0, padx=3, pady=3)

    
    upperWindow.columnconfigure([0], weight=1, minsize=75)
    upperWindow.rowconfigure([0,1,2,3], weight=1, minsize=50)
#End of Upper Window

#Lists the USB serial ports of the device
def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports

#Finds the arduino's USB port from the provided list, if none exist it returns None
def findArduino(ports):
    comm = None
    for port in ports:
        if 'arduino' in str(port.manufacturer):
            comm = port.device
    return comm

#connects to the arduio by calling get_ports() and findArduino()
def connect_arduino():
    global arduino
    global arduinoConnected
    
    if(arduinoConnected == False):
        port = findArduino(get_ports())
        if port == None:
            print("error, arduino not connected")
            return
        else:
            #arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout = 0.1)  #Default port for the Raspberrypi when the arduino is connected
            arduino = serial.Serial(port=port, baudrate=115200, timeout=0.1)
            connect_button.config(bg = 'green')
            connect_button.config(text = 'Arduino\nConnected')
            arduinoConnected = True
         
            
#Tracks if the arduino is connected yet
arduinoConnected = False

#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
#The base declartion of the array for values to be stored into
#Time, O2, CO2, Temp, Humidity, Pressure, O2Solenoid Time, CO2Solenoid Time
splitFloat = [0,0,0,0,0,0,0,0]
pressure = 0
## make a window
window = tk.Tk()
read_Settings()
#Title the window
window.title("Hypoxia Chamber GUI")
window.configure(bg='gold')
FileName = ""

##Place some Title text at the top of the window
intro_frame = tk.Frame()
intro_label = tk.Label(master = intro_frame, text = "Low-Cost Controlable Hypoxia Chamber \n HYPEngineers \n University of Idaho", font=("Arial",15), bg=("gold")).grid()


#Make some frames to contain all the desired features of the GUI
Target_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black", width = 100, height =10000)
oxyframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
carbframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
pressframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
fileframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
current_display_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")
setbutton_frame = tk.Frame(master = Target_frame)
gobutton_frame = tk.Frame()
settings_frame = tk.Frame(bg="gold")
errorbox_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")

# Make a function combiner so that a button can perform multiple commands:
def combineFunc(*funcs):
       def combinedFunc(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
       return combinedFunc

#Make a title for the input frame
target_title = tk.Label(master = Target_frame, text = 'Input Target Values', font = (1), fg="gold",bg="black")
target_title.grid(row = 0, columnspan = 2, padx=5, pady=5)

#Make a place to input the oxygen percentage
o2_label = tk.Label(master = oxyframe, text = "Percent Oxygen", fg="gold",bg="black").grid(row=1, column=0)
o2_entry = tk.Entry(master = oxyframe)
preload_Text(o2_entry, O2_Preload)
o2_entry.grid(row=2, column = 0, padx=5, pady=5) #create a textbox where the percent oxygen can be input

#Make a place to input the CO2 percentage
co2_label = tk.Label(master = carbframe, text = "Percent Carbon Dioxide", fg="gold",bg="black").grid() # label for co2 input entry
co2_entry = tk.Entry(master = carbframe)
preload_Text(co2_entry, CO2_Preload)
co2_entry.grid( padx=5, pady=5)

# Make a place to inut pressure calibration step
press_label = tk.Label(master =pressframe, text = "Pressure Calibration", fg="gold",bg="black").grid()
press_entry = tk.Entry(master = pressframe)
preload_Text(press_entry, Pres_Preload)
press_entry.grid( padx=5, pady=5)

## Make a place to input a file path and file name
pathlabel = tk.Label(master = fileframe, text = 'Folder path to save data to:', fg="gold",bg="black")
path_entry = tk.Entry(master = fileframe, width = 50)
preload_Text(path_entry, filePath_Preload)
file_name_label = tk.Label(master = (fileframe), text = 'Insert file name here:', fg="gold",bg="black")
file_name_entry = tk.Entry(master=(fileframe), width = 50)
preload_Text(file_name_entry, filename_Preload)

def browsefunc():
    global FileName
    filename = filedialog.askdirectory()
    if path_entry.cget('fg') == 'grey':
        path_entry.delete(0, "end") # delete all the text in the entry
        path_entry.config(fg = 'black')
    if len(path_entry.get()) == 0:
        timestamp = datetime.datetime.now()
        FileName = filename + '/' + timestamp.strftime("%m%d%y_%H%M") + '_' + file_name_entry.get() + '.csv'
        path_entry.insert(0, FileName)
    else:
        pass
    
browsebutton = tk.Button(master = fileframe, text="Browse", background = ('silver'), command= browsefunc)

# Grab File path
def path_graber():
    path_text = path_entry.get()
    print(path_text)

submit_button = tk.Button(master = fileframe, text = 'Submit file path', background = ('silver'), command = path_graber)

pathlabel.grid(columnspan =4, padx=5, pady=5)
browsebutton.grid(row = 3, column = 0, padx=5, pady=5)
file_name_label.grid(row = 1, column = 0)
file_name_entry.grid(row = 1, column = 1, columnspan = 2)
path_entry.grid(row = 3, column = 1, columnspan = 2, padx=5, pady=5)
submit_button.grid(row = 4, column = 1, padx=5, pady=5)

def exportBrowse():
    filename = filedialog.askdirectory()
    export_to_USB(FileName,filename)

# Make a button to transfer the file to a different location
transferbutton = tk.Button(master = fileframe, text = "Export file", background = ('silver'), command = exportBrowse)
transferbutton.grid(row = 4, column = 2)

# Make a label to display the accepted target values
o2_accepted = tk.Label(master = oxyframe, text = 'Current Target Value:'+ '-' +'%', fg="gold",bg="black")
o2_accepted.grid(padx=5, pady=5)
co2_accepted = tk.Label(master = carbframe, text = 'Current Target Value:'+'-'+'%', fg="gold",bg="black")
co2_accepted.grid(padx=5, pady=5)
press_accepted = tk.Label(master = pressframe, text = 'Current Target Value:'+'-'+'mBar', fg="gold",bg="black")
press_accepted.grid(padx=5, pady=5)

# Make the button grab the entered values when clicked
def entry_graber(event):
    global notification_msg
    global setvalues_button
    global o2_entry
    global co2_entry
    global o2_accepted
    global co2_accepted
    global press_accepted
    if setvalues_button['text'] == "Set Values":
        setvalues_button['text'] = 'Values gathered'
        target_o2 = float(o2_entry.get()) #assigns the input target o2 percentage to a variable
        target_co2 = float(co2_entry.get())
        if (target_o2 > 21):
            notification_msg['text'] = 'Oxygen value too high!'
            notification_msg['foreground']="red"
            notification_msg['bg']="black"
        elif (target_co2 > 100):
            notification_msg['text'] = 'Carbon dioxide value too high!'
            notification_msg['foreground']="red"
            notification_msg['bg']="black"
        else:
            notification_msg['text'] = "Target gas values accepted. Press 'Begin Experiment' to start."
            notification_msg['foreground']="green"
            notification_msg['bg']="black"
            o2_accepted['text'] = ('Current Target Value: '+ o2_entry.get() +'%')
            co2_accepted['text'] = ('Current Target Value: '+ co2_entry.get() +'%')
            press_accepted['text'] = ('Current Target Value: '+ press_entry.get() +'mBar')
            print(target_o2)
            write_O2(target_o2)
            print(target_co2)
            write_CO2(target_co2)
    else:
        setvalues_button['text'] = "Set Values"

#Make a button to set the target gas values and begin the chamber
setvalues_button = tk.Button(master = setbutton_frame, text="Set values", background = ('silver'), width = 15, height = 1, relief = "ridge", borderwidth = 5, fg="black")
setvalues_button.bind('<Button-1>', entry_graber)
setvalues_button.grid()

## Make a box to display notifications
notification_msg = tk.Label(master = errorbox_frame, height = 3, text = 'Any notifications will appear here.', bg="black", fg="gold")
notification_msg.grid(padx=5, pady=5)

####Make display values of the current conditions in the chamber
conditions_label = tk.Label(master = current_display_frame, text = "Current Conditions", font = (1), fg="gold",bg="black")
conditions_label.grid(padx=5, pady=5)

#Display the current o2 values
cond_o2_label = tk.Label(master = current_display_frame, text = "-", font =1, fg="gold",bg="black")
cond_o2_name = tk.Label(master = current_display_frame, text = "Current percent oxygen", fg="gold",bg="black")
cond_o2_name.grid(padx=5, pady=5)
cond_o2_label.grid(padx=5, pady=5)

#Display the current co2 values
cond_co2_label = tk.Label(master = current_display_frame, text = "-", font =1, fg="gold",bg="black")
cond_co2_name = tk.Label(master = current_display_frame, text = "Current percent carbon dioxide", fg="gold",bg="black")
cond_co2_name.grid(padx=5, pady=5)
cond_co2_label.grid(padx=5, pady=5)

#Display the current temperature
cond_temp_label = tk.Label(master = current_display_frame, text = "-", font =1, fg="gold",bg="black")
cond_temp_name = tk.Label(master = current_display_frame, text = "Current temperature in Celsius", fg="gold",bg="black")
cond_temp_name.grid(padx=5, pady=5)
cond_temp_label.grid(padx=5, pady=5)

#Display the current humidity
cond_humid_label = tk.Label(master = current_display_frame, text = "-", font =1, fg="gold",bg="black")
cond_humid_name = tk.Label(master = current_display_frame, text = "Current percent relative humidity", fg="gold",bg="black")
cond_humid_name.grid(padx=5, pady=5)
cond_humid_label.grid(padx=5, pady=5)

#Display the current pressure
cond_press_label = tk.Label(master = current_display_frame, text = "-", font =1, fg="gold",bg="black")
cond_press_name = tk.Label(master = current_display_frame, text = "Current pressure in mBar", fg="gold",bg="black")
cond_press_name.grid(padx=5, pady=5)
cond_press_label.grid(padx=5, pady=5)
cond_press_label['text'] = 0

#Update the current conditions display (currently it just cycles through random integers)
def display_updater():
    global cond_co2_label
    global cond_o2_label
    global cond_temp_label
    global cond_humid_label
    global cond_press_label
    global press_entry
    global window
    global after_ID
    global cond_press_label
    
    if(go_button['text'] == 'Experiment in progress...program is running. \n Press to end Experiment.'):
        splitFloat, data = read_ArduinoLine()
        if(splitFloat[0] != 0):
            #pressure = splitFloat[5]
            if(splitFloat[1] != 100):
                cond_o2_label['text'] = splitFloat[1]
            cond_co2_label['text'] = splitFloat[2]
            cond_temp_label['text'] = splitFloat[3]
            cond_humid_label['text'] = splitFloat[4]
            cond_press_label['text'] = splitFloat[5]
            write_CSV(splitFloat, FileName)
        
        
        if float(cond_press_label['text']) > float(press_entry.get()):
            notification_msg['text'] = 'Caution: Pressure exceeds set value! Exercise caution!'
            notification_msg['foreground']="red"
            notification_msg['bg']="black"
        else:
            notification_msg['text'] = 'Any notifications will appear here.'
            notification_msg['foreground']="gold"
            notification_msg['bg']="black"
        try:
            after_ID = window.after(100, display_updater) # To avoid errors with .after method, make it a global variable and use .after_cancel (when the window is closed)
            after_ID
        except:
            pass
    else:
        window.after_cancel(after_ID)


###Make a button to begin the hypoxia process (an experiment)
def toggle_gobutton_appearance():
    if (go_button['text'] == 'Begin Experiment'):
        go_button['text'] = 'Experiment in progress...program is running. \n Press to end Experiment.'
        go_button['background']="red"
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
        write_StartStopPause("Start")
    else:
        window.after_cancel(after_ID)
        go_button['text'] = 'Begin Experiment'
        notification_msg['text'] = 'Any notifications will appear here.'
        go_button['background']="green"
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
        write_StartStopPause("Stop")
        
go_button = tk.Button(master = gobutton_frame, text="Begin Experiment", background=("green"), width = 40, height = 2, relief = "ridge", borderwidth = 5, command = lambda:[toggle_gobutton_appearance(), display_updater()])
go_button.grid()

#Make a button to pause and un-pause the hypoxia process (an experiment)
def toggle_pausebutton_appearance():
    if (pause_button['text'] == "Pause Experiment"):
        pause_button['text'] = 'Experiment paused. Press to resume.'
        notification_msg['text'] = 'Program is paused. Door may be opened.'
        write_StartStopPause("Pause")
    else:
        pause_button['text'] = "Pause Experiment"
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'
        write_StartStopPause("Pause")

pause_button = tk.Button(master = gobutton_frame, text = "Pause Experiment", background = ('silver'), width = 40, height = 1, relief = 'ridge', borderwidth = 5, command = toggle_pausebutton_appearance)
pause_button.grid()  

settings_button = tk.Button(master = settings_frame, text = "PID Settings", background = ('silver'), width = 10, height = 2, relief = 'ridge', borderwidth = 5,command=create_window)
settings_button.grid(row=0, column = 0, padx=5, pady=5) 

save_settings_button = tk.Button(master = settings_frame, text = "Save Settings\nTo File", background = ('silver'), width = 10, height = 2, relief = 'ridge', borderwidth = 5,command=write_Settings)
save_settings_button.grid(row=0, column = 1, padx=5)  

Load_settings_button = tk.Button(master = settings_frame, text = "Load Settings\nFrom File", background = ('silver'), width = 10, height = 2, relief = 'ridge', borderwidth = 5)
Load_settings_button.bind('<Button>',lambda eff: read_Settings(eff, o2_entry, co2_entry, press_entry))
Load_settings_button.grid(row=1, column = 1, padx=5)  

connect_button = tk.Button(master = settings_frame, text = "Connect\nArduino", background = ('red'), width = 10, height = 2, relief = 'ridge', borderwidth = 5,command=connect_arduino)
connect_button.grid(row=1, column = 0, padx=5, pady=5)  

#Display the frames

intro_frame.grid(columnspan = 2, padx=3, pady=3)
Target_frame.grid(row = 1, column = 0, padx=3, pady=3)
oxyframe.grid(row = 1, column =0, padx=3, pady=3)
carbframe.grid(row =1, column =1, padx=3, pady=3)
pressframe.grid(padx=3, pady=3)
setbutton_frame.grid(row = 2, column =1, padx=3, pady=3)
fileframe.grid(columnspan = 2, padx=3, pady=3)
current_display_frame.grid(row = 0, column = 1, rowspan = 4, padx=3, pady=3)
gobutton_frame.grid(row = 2, padx=3, pady=3)
settings_frame.grid(row = 3, column = 1, padx=3, pady=3)
errorbox_frame.grid(row = 3, columnspan = 1, padx=3, pady=3)

#These lines make the frames adjust when the window size is changed
window.columnconfigure([0,1], weight=1, minsize=75)
window.rowconfigure([0,1,2,3], weight=1, minsize=50)

# Define what will happen when the window is closed.
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit? \n (Be sure to stop experiments before quitting!)"):
        window.destroy()
        if(arduinoConnected):
            arduino.close()

window.protocol("WM_DELETE_WINDOW", on_closing)

connect_arduino()

#Run the window for viewing
window.mainloop()





