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
import random
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from shutil import copy

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


def export_to_USB(src,dst):
    copy(src,dst)

def on_entry_click(eff=None, entry=None):
    """function that gets called whenever entry is clicked"""
    if entry != None:
        if entry.cget('fg') == 'grey':
           entry.delete(0, "end") # delete all the text in the entry
           entry.insert(0, '') #Insert blank for user input
           entry.config(fg = 'black')
def on_focusout(eff = None, entry = None, PreLoad = 'Filler'):
    if entry != None:
        if len(entry.get()) - entry.get().count(' ') < 1 :
            entry.insert(0, PreLoad)
            entry.config(fg = 'grey')

def preload_Text(entry = None, Preload = "Not Defined"):
    if(entry != None):
        entry.insert(0, Preload)
        entry.bind('<FocusIn>', lambda eff: on_entry_click(eff, entry))
        entry.bind('<FocusOut>', lambda eff: on_focusout(eff, entry, Preload))
        entry.config(fg = 'grey')

def create_window():
    upperWindow = tk.Toplevel(window)
    upperWindow.title("Hypoxia Chamber Settings GUI")
    upperWindow.configure(bg='gold')
   
    intro_frame = tk.Frame(master = upperWindow)
    intro_label = tk.Label(master = intro_frame, text = "Control Settings", font=("Arial",15), bg=("gold"))
    intro_label.grid() 
   
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
        measureTime = float(measure_entry.get()) #assigns the input target o2 percentage to a variable
        KpO2 = float(KpO2_entry.get())
        KiO2 = float(KiO2_entry.get())
        KpCO2 = float(KpCO2_entry.get())
        KiCO2 = float(KiCO2_entry.get())
        print(measureTime)
        print(KpO2)
        print(KiO2)
        print(KpCO2)
        print(KiCO2)
        
        #write_arduino("time " + measureTime)
        #write_arduino("KpO2 " + KpO2)
        #write_arduino("KiO2 " + KiO2)
        #write_arduino("KpCO2 " + KpCO2)
        #write_arduino("KiCO2 " + KiCO2)
        
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

FileName = ''
## make a window
window = tk.Tk()

#Title the window
window.title("Hypoxia Chamber GUI")
window.configure(bg='gold')

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
settings_frame = tk.Frame()
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
    if len(path_entry.get()) == 0:
        timestamp = datetime.now()
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
            print(target_co2)
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
    cond_o2_label['text'] = f'{random.randint(0, 20)}'
    cond_co2_label['text'] = f'{random.randint(0, 20)}'
    cond_temp_label['text'] = f'{random.randint(0, 20)}'
    cond_humid_label['text'] = f'{random.randint(0, 20)}'
    cond_press_label['text'] = f'{random.randint(0, 20)}'
    if(go_button['text'] == 'Experiment in progress...program is running. \n Press to end Experiment.'):
        if float(cond_press_label['text']) > float(press_entry.get()):
            notification_msg['text'] = 'Caution: Pressure exceeds set value! Exercise caution!'
            notification_msg['foreground']="red"
            notification_msg['bg']="black"
        else:
            notification_msg['text'] = 'Any notifications will appear here.'
            notification_msg['foreground']="gold"
            notification_msg['bg']="black"
        try:
            after_ID = window.after(1000, display_updater) # To avoid errors with .after method, make it a global variable and use .after_cancel (when the window is closed)
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
    else:
        window.after_cancel(after_ID)
        go_button['text'] = 'Begin Experiment'
        notification_msg['text'] = 'Any notifications will appear here.'
        go_button['background']="green"
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
        
go_button = tk.Button(master = gobutton_frame, text="Begin Experiment", background=("green"), width = 40, height = 2, relief = "ridge", borderwidth = 5, command = lambda:[toggle_gobutton_appearance(), display_updater()])
go_button.grid()

#Make a button to pause and un-pause the hypoxia process (an experiment)
def toggle_pausebutton_appearance():
    if (pause_button['text'] == "Pause Experiment"):
        pause_button['text'] = 'Experiment paused. Press to resume.'
        notification_msg['text'] = 'Program is paused. Door may be opened.'
    else:
        pause_button['text'] = "Pause Experiment"
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'

pause_button = tk.Button(master = gobutton_frame, text = "Pause Experiment", background = ('silver'), width = 40, height = 1, relief = 'ridge', borderwidth = 5, command = toggle_pausebutton_appearance)
pause_button.grid()   


settings_button = tk.Button(master = settings_frame, text = "Settings", background = ('silver'), width = 10, height = 2, relief = 'ridge', borderwidth = 5,command=create_window)
settings_button.grid()     

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
errorbox_frame.grid(row = 3, columnspan = 2, padx=3, pady=3)


#These lines make the frames adjust when the window size is changed
window.columnconfigure([0,1], weight=1, minsize=75)
window.rowconfigure([0,1,2,3], weight=1, minsize=50)

# Define what will happen when the window is closed.
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit? \n (Be sure to stop experiments before quitting!)"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

#Run the window for viewing
window.mainloop()