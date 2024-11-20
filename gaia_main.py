from math import trunc

from world import World

from tileset import Tileset

from tkinter import *
from tkinter import ttk

# ~~ Variables ~~

layer = 5

# ~~ Window instantiated/Window frame ~~
root_title = 'GAIA' # Variable for the window name
root = Tk()
root.title(root_title)
frm = ttk.Frame(root, padding=10)
frm.grid()

Mappy = World()
tileset = Tileset(5)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# Styling TTK

bd_frm = ttk.Style()
bd_frm.configure("top_frm.TFrame", background="black")

# GUI Frames
right_frm = ttk.Frame(frm)
top_frm = ttk.Frame(frm, style="top_frm.TFrame", borderwidth=1)
canvas_frm = ttk.Frame(top_frm)
bottom_frm = ttk.Frame(frm)

## Configuring proportions
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=2)

right_frm.grid(column=1, columnspan=2, sticky="e")
top_frm.grid(column=0, row=0, sticky="n")
bottom_frm.grid(column=0,row=1, sticky="s")
canvas_frm.pack()


# Settings Widgets
settings_label = ttk.Label(right_frm, text="Settings")
settings_label.grid(row=0, column=0 ,columnspan=2, sticky="n")

seedyVar = StringVar()
seed_label = ttk.Label(right_frm, text="Seed:")
seed_entry = ttk.Entry(right_frm, textvariable=seedyVar)
seed_label.grid(row=1, column=0, sticky="e")
seed_entry.grid(row=1, column=1, sticky="w")


small_button = ttk.Button(right_frm, text="small")
medium_button = ttk.Button(right_frm, text="medium")
large_button = ttk.Button(right_frm, text="large")
small_button.grid(row=2, column=0, sticky="e")
medium_button.grid(row=2, column=1, sticky="s")
large_button.grid(row=2, column=2, sticky="w")

generate_button = ttk.Button(right_frm, text="Start", command=lambda : tileset.drawTiles(Mappy.initiateGeneration(seedyVar), canvas))
generate_button.grid(row=3, column=1, sticky="s")

# Canvas Widgets
canvas = Canvas(canvas_frm, width=500, height=500, bg='lightgrey', border=0, highlightthickness = 0, highlightbackground = 'black')
canvas.pack()

#rectangle = canvas.create_rectangle(0, 0, 5, 5, outline="springgreen1", width=0, fill="springgreen1")

LeftButton = ttk.Button(bottom_frm, text = "Down", command=lambda : tileset.layerChange("Down"))
CentreButton = ttk.Button(bottom_frm, text = "Redisplay", command=lambda : tileset.drawTiles(Mappy.world_grid, canvas))
RightButton = ttk.Button(bottom_frm, text = "Right", command=lambda : tileset.layerChange("Up"))

LeftButton.pack(side=LEFT)
CentreButton.pack(side=LEFT)
RightButton.pack(side=LEFT)

# seedyVar = "123ABC"
# testingfile = open("idk.txt", "w")
# temp = Mappy.initiateGeneration(seedyVar)
# for x in temp[4]:
#     tmpstr = str(x) + "\n"
#     testingfile.write(tmpstr)S
# testingfile.close()

while True:
    root.update_idletasks()
    root.update()

### TESTING TO UNDERSTAND HOW GITHUB WORKS