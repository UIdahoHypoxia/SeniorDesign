# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:14:04 2021

@author: izzie-strawn
"""
# Start stop experiment and pause/continue experiment
# type in file name to store data in certain spot
# make pressure check to alarm when pressure is greater than value (have manual input for atmospheric pressure)


## import modules
import tkinter as tk
import random

window = None

## make a window
window = tk.Tk()

#Title the window
window.title("Hypoxia Chamber GUI")

##Place some instruction text at the top of the window
intro_frame = tk.Frame()
intro_label = tk.Label(master = intro_frame, text = "Low-Cost Controlable Hypoxia Chamber \n HYPEngineers \n University of Idaho").grid()


#Make some frames to contain all the desired features of the GUI
oxyframe = tk.Frame(relief = 'ridge', borderwidth = 5)
carbframe = tk.Frame(relief = 'ridge', borderwidth = 5)
current_display_frame = tk.Frame(relief = 'ridge', borderwidth = 5)
setbutton_frame = tk.Frame()
gobutton_frame = tk.Frame()
errorbox_frame = tk.Frame(relief = 'ridge', borderwidth = 5)

#Make a place to input the oxygen percentage
o2_label = tk.Label(master = oxyframe, text = "Percent Oxygen").grid(row=1, column=0)
o2_entry = tk.Entry(master = oxyframe)
o2_entry.grid(row=2, column = 0) #create a textbox where the percent oxygen can be input

#Make a place to input the CO2 percentage
co2_label = tk.Label(master = carbframe, text = "Percent Carbon Dioxide").grid() # label for co2 input entry
co2_entry = tk.Entry(master = carbframe)
co2_entry.grid()

#Make a button to set the target gas values and begin the chamber
setvalues_button = tk.Button(master = setbutton_frame, text="Set values", width = 10, height = 1, relief = "ridge", borderwidth = 5)
setvalues_button.grid()

## Make a box to display notifications
notification_msg = tk.Label(master = errorbox_frame, height = 3, text = 'Any notifications will appear here. Program not running.')
notification_msg.grid()

#Change the notification based on some inputs

#if (pressure > 100):
#    notification_msg['text'] = 'Warning: Pressure too high. Exercise caution.'


# Make the button grab the entered values when clicked
def entry_graber(event):
    global notification_msg
    target_o2 = float(o2_entry.get()) #assigns the input target o2 percentage to a variable
    target_co2 = float(co2_entry.get())
    if (target_o2 > 21):
        notification_msg['text'] = 'Oxygen value too high!'
    elif (target_co2 > 100):
        notification_msg['text'] = 'Carbon dioxide value too high!'
    else:
        notification_msg['text'] = "Target gas values accepted. Press 'Begin' to start."
        print(target_o2)
        print(target_co2)

setvalues_button.bind("<Button-1>", entry_graber)


####Make display values of the current conditions in the chamber
conditions_label = tk.Label(master = current_display_frame, text = "Current Conditions")
conditions_label.grid()

#Display the current o2 values
cond_o2_label = tk.Label(master = current_display_frame, text = "-")
cond_o2_name = tk.Label(master = current_display_frame, text = "Current percent oxygen")
cond_o2_name.grid()
cond_o2_label.grid()

#Display the current co2 values
cond_co2_label = tk.Label(master = current_display_frame, text = "-")
cond_co2_name = tk.Label(master = current_display_frame, text = "Current percent carbon dioxide")
cond_co2_name.grid()
cond_co2_label.grid()

#Update the current conditions display (currently it just cycles through random integers)
def display_updater():
    global cond_co2_label
    global cond_o2_label
    global window
    #if 'normal' == window.state():
    cond_o2_label['text'] = f'{random.randint(0, 20)}'
    cond_co2_label['text'] = f'{random.randint(0, 20)}'

    window.after(1000, display_updater)
    #else:
     #   pass

#Collect and display data button
collect_button = tk.Button(master= gobutton_frame, text = 'Press to collect data', command = display_updater)
collect_button.grid()
#window.after(1000, display_updater) ## These lines give errors 'invalid command name'. This is because the code tries to run this function and update the widgets after the window is closed. Basically, it is working fine, but there errors are annoying.

###Make a button to begin the hypoxia process (pauses when not pushed - default = paused, pushed = chamber is changing gas composition)
def toggle_gobutton_appearance():
    if (go_button['text'] == 'Begin'):
        go_button['text'] = 'Program is running...Press to Pause'
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'
    else:
        go_button['text'] = 'Begin'
        notification_msg['text'] = 'Any notifications will appear here. Program not running.'
        
go_button = tk.Button(master = gobutton_frame, text="Begin", width = 40, height = 1, relief = "ridge", borderwidth = 5, command = toggle_gobutton_appearance)
go_button.grid()
    
#Display the frames
intro_frame.grid(columnspan = 2)
oxyframe.grid(row=1, column=0)
carbframe.grid(row=2, column=0)
setbutton_frame.grid(row=3, column=0)
current_display_frame.grid(row = 1, column = 1, rowspan = 4)
gobutton_frame.grid(row = 4)
errorbox_frame.grid(row = 5, columnspan = 2)

#These lines make the frames adjust when the window size is changed
window.columnconfigure([0,1], weight=1, minsize=75)
window.rowconfigure([0,1,2,3], weight=1, minsize=50)

#Run the window for viewing
window.mainloop()