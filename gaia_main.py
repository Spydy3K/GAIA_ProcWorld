from math import trunc

from world import World

from tkinter import *
from tkinter import ttk

# ~~ Window instantiated/Window frame ~~
root_title = 'GAIA' # Variable for the window name
root = Tk()
root.title(root_title)
frm = ttk.Frame(root, padding=10)
frm.grid()

Mappy = World()

#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# GUI Frames
right_frm = ttk.Frame(frm)
top_frm = ttk.Frame(frm)
bottom_frm = ttk.Frame(frm)

## Configuring proportions
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=2)

right_frm.grid(column=1, columnspan=2, sticky="e")
top_frm.grid(column=0, row=0, sticky="ne")
bottom_frm.grid(column=0,row=1, sticky="s")


# Settings Widgets
settings_label = ttk.Label(right_frm, text="Settings").grid(row=0, column=0 ,columnspan=2, sticky="n")

seedyVar = StringVar()
seed_label = ttk.Label(right_frm, text="Seed:").grid(row=1, column=0, sticky="e")
seed_entry = ttk.Entry(right_frm, textvariable=seedyVar).grid(row=1, column=1, sticky="w")

small_button = ttk.Button(right_frm, text="small").grid(row=2, column=0)
medium_button = ttk.Button(right_frm, text="medium").grid(row=2, column=1)
large_button = ttk.Button(right_frm, text="large").grid(row=2, column=2)

generate_button = ttk.Button(right_frm, text="Start", command=lambda : Mappy.initiateGeneration(seedyVar)).grid(row=3, column=1, sticky="s")

# Generation Widgets
GenerationCanvas = Canvas(top_frm, width=1000, height=1000, bg='Red', border=1, borderwidth=5)
GenerationCanvas.create_line(10, 10, 1000, 1000)
LeftButton = ttk.Button(bottom_frm, text = "Left", padding=5).grid(row=0, column=0, sticky="e")
CentreButton = ttk.Button(bottom_frm, text = "Centre", padding=5).grid(row=0, column=1, sticky="nsew")
RightButton = ttk.Button(bottom_frm, text = "Right", padding=5).grid(row=0, column=2, sticky="w")

label1 = ttk.Label(top_frm, text = "1")

root.mainloop()

### TESTING TO UNDERSTAND HOW GITHUB WORKS