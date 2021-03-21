# -*- coding: utf-8 -*-
"""
This script creates a basic window using Tkinter, and sets up the layout of
the different componenets that we will need. No interactions have been set up
yet - just some infrastructure.
Script by: izzie-strawn
"""

import tkinter as tk #import tkinter module
window = tk.Tk() #create the GUI window

#Title the window
window.title("Hypoxia Chamber")

#Place some text at the top of the window
title_label = tk.Label(text = "Hypoxia Chamber GUI") #Write some text in the window
title_label.pack()#add the text to the window

#Make some containers (frames)
oxyframe = tk.Frame(relief = 'ridge', borderwidth = 5)#makes a container with a border effect
carbframe = tk.Frame(relief = 'ridge', borderwidth = 5)# makes another container
current_display_frame = tk.Frame(relief = 'ridge', borderwidth = 5) # make frame for current values

#Make a place to input the oxygen percentage
o2_label = tk.Label(master = oxyframe, text = "Percent Oxygen") #label for oxygen input entry
o2_label.pack()
o2_entry = tk.Entry(master = oxyframe) #create a textbox where the percent oxygen can be input
o2_entry.pack()
target_o2 = o2_entry.get() #assigns the input target o2 percentage to a variable

#Make a place to input the CO2 percentage
co2_label = tk.Label(master = carbframe, text = "Percent Carbon Dioxide") # label for co2 input entry
co2_label.pack()
co2_entry = tk.Entry(master = carbframe)
co2_entry.pack()
target_co2 = co2_entry.get()

#Make display values of the current conditions in the chamber
### insert code that displays current conditions in the chamber (&graphs it possibly)

#Display the frames that were created
oxyframe.pack() 
carbframe.pack()
current_display_frame.pack()

#Make a button to set the target gas values and begin the chamber
go_button = tk.Button(text="Go!", width = 10, height = 1, relief = "ridge", borderwidth = 5)
go_button.pack()


window.mainloop() #this line makes the window appear and function

###insert code that cause reactions when the button is pressed

