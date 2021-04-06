# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:14:04 2021
@authors: izzie strawn, colin marchus, jacob knudson

Progress notes:
*Error with pressure calibration - need to set it to not collect input until button is pushed.
*Idea: Make a seperate button to set the pressure value and compare that data
*Make conditions not update until begin button pressed - accomplished with a few bugs
*Why does setvalues_button need to be pressed twice? something is wrong...

"""

## import modules
import tkinter as tk
import random
from tkinter import filedialog
from tkinter import messagebox

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
errorbox_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")

# Make a function combiner so that a button can perform multiple commands:
def combineFunc(*funcs):
       def combinedFunc(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
       return combinedFunc

#Make a title for the input frame
target_title = tk.Label(master = Target_frame, text = 'Input Target Values')
target_title.grid()

#Make a place to input the oxygen percentage
o2_label = tk.Label(master = oxyframe, text = "Percent Oxygen", fg="gold",bg="black").grid(row=1, column=0)
o2_entry = tk.Entry(master = oxyframe)
o2_entry.grid(row=2, column = 0) #create a textbox where the percent oxygen can be input

#Make a place to input the CO2 percentage
co2_label = tk.Label(master = carbframe, text = "Percent Carbon Dioxide", fg="gold",bg="black").grid() # label for co2 input entry
co2_entry = tk.Entry(master = carbframe)
co2_entry.grid()

# Make a place to inut pressure calibration step
press_label = tk.Label(master =pressframe, text = "Pressure Calibration", fg="gold",bg="black").grid()
press_entry = tk.Entry(master = pressframe)
press_entry.grid()


## Make a place to input a file path
pathlabel = tk.Label(master = fileframe, text = 'Insert file path')
path_entry = tk.Entry(master = fileframe)

def browsefunc():
    filename = filedialog.askopenfilename()
    path_entry.insert(0, filename)
    
browsebutton = tk.Button(master = fileframe, text="Browse", command=browsefunc)

# Grab File path
def path_graber():
    path_text = path_entry.get()
    print(path_text)

submit_button = tk.Button(master = fileframe, text = 'Submit file path', command = path_graber)

pathlabel.grid(columnspan =3)
browsebutton.grid(row = 1, column = 0)
path_entry.grid(row = 1, column = 1)
submit_button.grid(row = 2)

# Make a label to display the accepted target values
o2_accepted = tk.Label(master = oxyframe, text = 'Current Target Value:'+ '-' +'%')
o2_accepted.grid()
co2_accepted = tk.Label(master = carbframe, text = 'Current Target Value:'+'-'+'%')
co2_accepted.grid()

# Make the button grab the entered values when clicked
def entry_graber(event):
    global notification_msg
    global setvalues_button
    global o2_entry
    global co2_entry
    global o2_accepted
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
            print(target_o2)
            print(target_co2)
    else:
        setvalues_button['text'] = "Set Values"

#Make a button to set the target gas values and begin the chamber
setvalues_button = tk.Button(master = setbutton_frame, text="Set values", width = 15, height = 1, relief = "ridge", borderwidth = 5, fg="gold",bg="black")
setvalues_button.bind('<Button-1>', entry_graber)
setvalues_button.grid()

## Make a box to display notifications
notification_msg = tk.Label(master = errorbox_frame, height = 3, text = 'Any notifications will appear here.', bg="black", fg="gold")
notification_msg.grid()

####Make display values of the current conditions in the chamber
conditions_label = tk.Label(master = current_display_frame, text = "Current Conditions", font = (1), fg="gold",bg="black")
conditions_label.grid()

#Display the current o2 values
cond_o2_label = tk.Label(master = current_display_frame, text = "-", fg="gold",bg="black")
cond_o2_name = tk.Label(master = current_display_frame, text = "Current percent oxygen", fg="gold",bg="black")
cond_o2_name.grid()
cond_o2_label.grid()

#Display the current co2 values
cond_co2_label = tk.Label(master = current_display_frame, text = "-", fg="gold",bg="black")
cond_co2_name = tk.Label(master = current_display_frame, text = "Current percent carbon dioxide", fg="gold",bg="black")
cond_co2_name.grid()
cond_co2_label.grid()

#Display the current temperature
cond_temp_label = tk.Label(master = current_display_frame, text = "-", fg="gold",bg="black")
cond_temp_name = tk.Label(master = current_display_frame, text = "Current temperature in Celsius", fg="gold",bg="black")
cond_temp_name.grid()
cond_temp_label.grid()

#Display the current humidity
cond_humid_label = tk.Label(master = current_display_frame, text = "-", fg="gold",bg="black")
cond_humid_name = tk.Label(master = current_display_frame, text = "Current percent relative humidity", fg="gold",bg="black")
cond_humid_name.grid()
cond_humid_label.grid()

#Display the current pressure
cond_press_label = tk.Label(master = current_display_frame, text = "-", fg="gold",bg="black")
cond_press_name = tk.Label(master = current_display_frame, text = "Current pressure in mBar", fg="gold",bg="black")
cond_press_name.grid()
cond_press_label.grid()

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
    cond_o2_label['text'] = f'{random.randint(0, 20)}'
    cond_co2_label['text'] = f'{random.randint(0, 20)}'
    cond_temp_label['text'] = f'{random.randint(0, 20)}'
    cond_humid_label['text'] = f'{random.randint(0, 20)}'
    cond_press_label['text'] = f'{random.randint(0, 20)}'
    if(go_button['text'] == 'Experiment in progress...program is running. \n Press to end Experiment.'):
        try:
            after_ID = window.after(100, display_updater) # To avoid errors with .after method, make it a global variable and use .after_cancel (when the window is closed)
            after_ID
        except:
            pass
    else:
        window.after_cancel(after_ID)



#display_updater()
'''
## Make notification box react to pressure values
def pressure_compare():
    global notification_msg
    global cond_press_label
    try:
        if float(cond_press_label['text']) > float(press_entry.get()):
            notification_msg['text'] = 'Caution: Pressure exceeds set value! Exercise caution!'
            notification_msg['foreground']="red"
            notification_msg['bg']="black"
        else:
            notification_msg['text'] = 'Any notifications will appear here.'
            notification_msg['foreground']="gold"
            notification_msg['bg']="black"
    except:
        notification_msg['text'] = 'Please input pressure calibration'
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
'''
def toggle_press_button_appearance():
    global notification_msg
    global cond_press_label
    try:
        if (press_button['text'] == 'Set Base Pressure'):
            press_button['text'] = ('Base Pressure set to' + press_entry.get() + 'mBar')
            if float(cond_press_label['text']) > float(press_entry.get()):
                notification_msg['text'] = 'Caution: Pressure exceeds set value! Exercise caution!'
                notification_msg['foreground']="red"
                notification_msg['bg']="black"
            else:
                notification_msg['text'] = 'Any notifications will appear here.'
                notification_msg['foreground']="gold"
                notification_msg['bg']="black"
        else:
            press_button['text'] = 'Set Base Pressure'
    except:
        notification_msg['text'] = 'Please input pressure calibration'
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"

# Make a button to set pressure calibration
press_button = tk.Button(master = pressframe, text = 'Set Base Pressure', command = toggle_press_button_appearance)
press_button.grid()

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

pause_button = tk.Button(master = gobutton_frame, text = "Pause Experiment", background = ('gold'), width = 40, height = 1, relief = 'ridge', borderwidth = 5, command = toggle_pausebutton_appearance)
pause_button.grid()    

#Display the frames

intro_frame.grid(columnspan = 2)
Target_frame.grid(row = 1, column = 0)
oxyframe.grid()
carbframe.grid()
pressframe.grid()
fileframe.grid()
setbutton_frame.grid()
current_display_frame.grid(row = 1, column = 1, rowspan = 4)
gobutton_frame.grid(row = 5)
errorbox_frame.grid(row = 6, columnspan = 2)

#These lines make the frames adjust when the window size is changed
window.columnconfigure([0,1], weight=1, minsize=75)
window.rowconfigure([0,1,2,3], weight=1, minsize=50)

# Define what will happen when the window is closed.
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #try:
         #   window.after_cancel(after_ID)
        #except:
         #   window.after_cancel(display_updater)
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

#Run the window for viewing
window.mainloop()