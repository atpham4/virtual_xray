import matplotlib.pyplot as plt
import numpy as np
import math
from tkinter import *

from phantom import generate_2d_phantom, generate_bigger_broken_leg, generate_leg, generate_3d_phantom, generate_tissue, generate_broken_leg, get_2d_profile, intensity_function, intensity_line_graph

#Simple GUI to input values to run code
def runGUI():
    window = Tk()   
    window.title('X-Ray GUI')
    window.geometry('500x500')
    
    Label(window, text = "X-Ray configuration", font=("Helvetica", 12), anchor = "w").grid(stick= 'W', row = 0, column = 0)
        
    Label(window, text = "Enter a X-Ray Energy value: ").grid(stick= 'W', row = 1, column = 0)
    xray_intensity = StringVar()
    set1 = OptionMenu(window, xray_intensity, "20", "30", "40").grid(row = 1, column = 1)
    xray_intensity.set("20")

    Label(window, text = "Enter a X-Ray angle value: ").grid(stick= 'W', row = 2, column = 0)
    xray_angle = StringVar()
    set2 = OptionMenu(window, xray_angle, "20", "30", "40", "60", "80", "90").grid(stick= 'W', row = 2, column = 1)
    xray_angle.set("90")

    Label(window, text = "\nPhantom configuration", font=("Helvetica", 12), anchor = "w").grid(stick= 'W', row = 3, column = 0)
    
    Label(window, text = "Enter attenuation(u) of leg: ").grid(stick= 'W', row = 4, column = 0)
    u_leg = StringVar()
    set3 = OptionMenu(window, u_leg, ".5", ".025", ".01").grid(row = 4, column = 1)
    u_leg.set(".5")

    Label(window, text = "Enter attenuation(u) of bone: ").grid(stick= 'W', row = 5, column = 0)
    u_bone = StringVar()
    set4 = OptionMenu(window, u_bone, ".99", ".90", ".85").grid(row = 5, column = 1)
    u_bone.set(".99")

    Label(window, text = "Leg condition: ").grid(stick = 'W', row = 6, column = 0)
    leg_condition = StringVar()
    set_leg_condition = OptionMenu(window, leg_condition, "Normal", "Broken", "Bigger Angled Slit").grid(row = 6, column = 1)
    leg_condition.set("Normal")

    Label(window, text = "Leg View: ").grid(stick = 'W', row = 7, column = 0)
    leg_angle = StringVar()
    set_leg_angle = OptionMenu(window, leg_angle, "Front", "Side").grid(row = 7, column = 1)
    leg_angle.set("Front")


    Label(window, text = "\nChange Distance", font=("Helvetica", 12), anchor = "w").grid(stick= 'W', row = 8, column = 0)
    
    Label(window, text = "Film to Phantom: ").grid(stick= 'W', row = 9, column = 0)
    film_to_phantom = StringVar()
    set5 = OptionMenu(window, film_to_phantom, "1", "2", "3", "4").grid(row = 9, column = 1)
    film_to_phantom.set("1")

    Label(window, text = "X-Ray Source to Phantom: ").grid(stick= 'W', row = 10, column = 0)
    source_to_phantom = StringVar()
    set6 = OptionMenu(window, source_to_phantom, "7", "6", "5", "4").grid(row = 10, column = 1)
    source_to_phantom.set("7")

    def clicked():
        total_length = int(source_to_phantom.get()) - int(film_to_phantom.get())
        test_phantom = generate_tissue(float(u_leg.get()), float(u_bone.get()))
        intensityList = intensity_function(float(xray_intensity.get()), test_phantom)
        
        leg_phantom = generate_leg(float(u_leg.get()), float(u_bone.get()))
        if leg_condition.get() == "Broken":
            leg_phantom = generate_broken_leg(float(u_leg.get()), float(u_bone.get()))
        elif leg_condition.get() == "Bigger Angled Slit":
            leg_phantom = generate_bigger_broken_leg(float(u_leg.get()), float(u_bone.get()))
        generate_3d_phantom(leg_phantom[0], leg_phantom[1])
        get_2d_profile(int(xray_intensity.get()), leg_phantom, total_length, int(xray_angle.get()), leg_angle.get())
        plt.show()
    
    btn = Button(window, text="Start", command=clicked)
    
    btn.grid(column=0, row=11)
    
    window.mainloop()

runGUI()

