from tkinter import *
from tkinter import ttk

#from perlin-noise import PerlinNoise

# ~~ Window instantiated/Window frame ~~
root_title = 'GAIA' # Variable for the window name
root = Tk()
root.title(root_title)
frm = ttk.Frame(root, padding=10)
frm.grid()

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

seed_label = ttk.Label(right_frm, text="Seed:").grid(row=1, column=0, sticky="e")
seed_entry = ttk.Entry(right_frm).grid(row=1, column=1, sticky="w")

small_button = ttk.Button(right_frm, text="small").grid(row=2, column=0)
medium_button = ttk.Button(right_frm, text="medium").grid(row=2, column=1)
large_button = ttk.Button(right_frm, text="large").grid(row=2, column=2)

generate_button = ttk.Button(right_frm, text="Start").grid(row=3, column=1, sticky="s")

# Generation Widgets
entryGenerator = ttk.Entry(top_frm, background="pink", width=50).grid()
LeftButton = ttk.Button(bottom_frm, text = "Left", padding=5).grid(row=0, column=0, sticky="e")
CentreButton = ttk.Button(bottom_frm, text = "Centre", padding=5).grid(row=0, column=1, sticky="nsew")
RightButton = ttk.Button(bottom_frm, text = "Right", padding=5).grid(row=0, column=2, sticky="w")

label1 = ttk.Label(top_frm, text = "1")

# # ~~ Grid generated ~~
# grid_size = 2
# world_grid = [] # Using an array because it is simple. Temp?
# type_emptycell = 1 ### DEBUGGING
# layerNo = 0

# # Generates an array based on variables given
# for layer in range(0, 11):
#     rowNo = 0
#     world_grid.append([])

#     for row in range(0, grid_size):
#         world_grid[layerNo].append([])

#         for column in range(0, grid_size):
#             world_grid[layerNo][rowNo].append(type_emptycell)
#             type_emptycell += 1 ### DEBUGGING to test what order values are added into the 2D array
#         rowNo += 1
#     layerNo += 1
# grid_print = True # Enables/Disables printing
# gen_count = 0

# while(grid_print):
#     layer_input = int(input("What layer would you like to see? [1 to 10]: "))
#     layer_print = world_grid[layer_input-1]
#     for z in layer_print: # Should be printing the rows...
#         print(z, end='\n')
#     grid_print = False # Concluded and so it will stop

# ~~ Generate map ~~



root.mainloop()

### TESTING TO UNDERSTAND HOW GITHUB WORKS