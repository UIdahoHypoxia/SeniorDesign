# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 09:14:04 2021

@author: izzie-strawn
"""
## import modules
import tkinter as tk

## make a window
window = tk.Tk()

#Title the window
window.title("Hypoxia Chamber GUI")

##Place some instruction text at the top of the window
intro_frame = tk.Frame(relief = 'ridge', borderwidth = 5)
intro_label = tk.Label( text = "Low-Cost Controlable Hypoxia Chamber \n HYPEngineers \n University of Idaho").grid(row=0, column=0)


#Make some frames to contain all the desired features of the GUI
oxyframe = tk.Frame(relief = 'ridge', borderwidth = 5)
carbframe = tk.Frame(relief = 'ridge', borderwidth = 5)
current_display_frame = tk.Frame(relief = 'ridge', borderwidth = 5)
button_frame = tk.Frame()

#Make a place to input the oxygen percentage
o2_label = tk.Label(master = oxyframe, text = "Percent Oxygen").grid(row=1, column=0)
o2_entry = tk.Entry(master = oxyframe)
o2_entry.grid(row=2, column = 0) #create a textbox where the percent oxygen can be input
target_o2 = o2_entry.get() #assigns the input target o2 percentage to a variable

#Make a place to input the CO2 percentage
co2_label = tk.Label(master = carbframe, text = "Percent Carbon Dioxide").grid() # label for co2 input entry
co2_entry = tk.Entry(master = carbframe)
co2_entry.grid()
target_co2 = co2_entry.get()

#Make a button to set the target gas values and begin the chamber
go_button = tk.Button(master = button_frame, text="Go!", width = 10, height = 1, relief = "ridge", borderwidth = 5)
go_button.grid()
go_button.bind("<Button-1>") #begin coding the function of the button

####Make display values of the current conditions in the chamber
conditions_label = tk.Label(master = current_display_frame, text = "Current Conditions")
conditions_label.grid()

#Display the current o2 values
cond_o2_label = tk.Label(master = current_display_frame, text = "21")
cond_o2_name = tk.Label(master = current_display_frame, text = "Current percent oxygen")
cond_o2_name.grid()
cond_o2_label.grid()

#Display the current co2 values
cond_co2_label = tk.Label(master = current_display_frame, text = "0")
cond_co2_name = tk.Label(master = current_display_frame, text = "Current percent carbon dioxide")
cond_co2_name.grid()
cond_co2_label.grid()


#Display the frames
intro_frame.grid(row=0, column = 0)
oxyframe.grid(row=1, column=0)
carbframe.grid(row=2, column=0)
button_frame.grid(row=3, column=0)
current_display_frame.grid(row = 1, column = 1)


window.mainloop()