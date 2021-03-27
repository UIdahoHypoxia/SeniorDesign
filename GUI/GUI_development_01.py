# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:14:04 2021
@authors: izzie strawn, colin marchus, jacob knudson

Progress notes:
*Still working on file input (line 51).
*Still need to figure out how to stop displaying error message.
*Error with pressure calibration - need to set it to not collect input until button is pushed.
"""

## import modules
import tkinter as tk
import random
#import pygame

## make a window
window = tk.Tk()

#Title the window
window.title("Hypoxia Chamber GUI")
window.configure(bg='gold')

##Place some instruction text at the top of the window
intro_frame = tk.Frame()
intro_label = tk.Label(master = intro_frame, text = "Low-Cost Controlable Hypoxia Chamber \n HYPEngineers \n University of Idaho", font=("Arial",15), bg=("gold")).grid()


#Make some frames to contain all the desired features of the GUI
Target_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")
oxyframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
carbframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
pressframe = tk.Frame(master = Target_frame, relief = 'ridge', borderwidth = 5, bg="black")
current_display_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")
setbutton_frame = tk.Frame()
gobutton_frame = tk.Frame()
errorbox_frame = tk.Frame(relief = 'ridge', borderwidth = 5, bg="black")

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

# Make a place to input a file name to save the sensor data to
filename_label = tk.Label(master = Target_frame, text = "Input file path").grid()
filename = tk.Entry(master = Target_frame)
filename.grid()

#Make a button to set the target gas values and begin the chamber
setvalues_button = tk.Button(master = setbutton_frame, text="Set values", width = 10, height = 1, relief = "ridge", borderwidth = 5, fg="gold",bg="black")
setvalues_button.grid()

## Make a box to display notifications
notification_msg = tk.Label(master = errorbox_frame, height = 3, text = 'Any notifications will appear here.', bg="black", fg="gold")
notification_msg.grid()

# Make the button grab the entered values when clicked
def entry_graber(event):
    global notification_msg

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
        notification_msg['text'] = "Target gas values accepted. Press 'Begin' to start."
        notification_msg['foreground']="green"
        notification_msg['bg']="black"
        print(target_o2)
        print(target_co2)

setvalues_button.bind("<Button-1>", entry_graber)

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
    cond_o2_label['text'] = f'{random.randint(0, 20)}'
    cond_co2_label['text'] = f'{random.randint(0, 20)}'
    cond_temp_label['text'] = f'{random.randint(0, 20)}'
    cond_humid_label['text'] = f'{random.randint(0, 20)}'
    cond_press_label['text'] = f'{random.randint(0, 20)}'
  
    ## Make notification box react to pressure values
    if float(cond_press_label['text']) > float(press_entry.get()):
        notification_msg['text'] = 'Caution: Pressure exceeds set value! Exercise caution!'
        notification_msg['foreground']="red"
        notification_msg['bg']="black"
    else:
        notification_msg['text'] = 'Any notifications will appear here.'
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
  
    window.after(1000, display_updater)

window.after(1000, display_updater)

###Make a button to begin the hypoxia process (an experiment)
def toggle_gobutton_appearance():
    if (go_button['text'] == 'Begin Experiment'):
        go_button['text'] = 'Experiment in progress...program is running.'
        go_button['background']="red"
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
    else:
        go_button['text'] = 'Begin Experiment'
        notification_msg['text'] = 'Any notifications will appear here.'
        go_button['background']="green"
        notification_msg['foreground']="gold"
        notification_msg['bg']="black"
go_button = tk.Button(master = gobutton_frame, text="Begin Experiment", background=("green"), width = 40, height = 1, relief = "ridge", borderwidth = 5, command = toggle_gobutton_appearance)
go_button.grid()

#Make a button to pause and un-pause the hypoxia process (an experiment)
def toggle_pausebutton_appearance():
    if (pause_button['text'] == "Pause Experiment"):
        pause_button['text'] = 'Experiment paused'
        notification_msg['text'] = 'Program is paused. Door may be opened.'
    else:
        pause_button['text'] = "Pause Experiment"
        notification_msg['text'] = 'Do not forget to pause the program to open the door.'

pause_button = tk.Button(master = gobutton_frame, text = "Pause Experiment", background = ('gold'), width = 40, height = 1, relief = 'ridge', borderwidth = 5, command = toggle_pausebutton_appearance)
pause_button.grid()    

#Display the frames

intro_frame.grid(columnspan = 2)
Target_frame.grid(row = 1, column = 0)
oxyframe.grid(row=1, column=0)
carbframe.grid(row=2, column=0)
pressframe.grid(row = 3, column = 0)
setbutton_frame.grid(row=4, column=0)
current_display_frame.grid(row = 1, column = 1, rowspan = 4)
gobutton_frame.grid(row = 5)
errorbox_frame.grid(row = 6, columnspan = 2)

#These lines make the frames adjust when the window size is changed
window.columnconfigure([0,1], weight=1, minsize=75)
window.rowconfigure([0,1,2,3], weight=1, minsize=50)

#Run the window for viewing
window.mainloop()