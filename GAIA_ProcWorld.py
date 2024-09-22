from tkinter import *
from tkinter import ttk

from hashlib import md5
from perlin_noise import PerlinNoise

# # ~~ Window instantiated/Window frame ~~
# root_title = 'GAIA' # Variable for the window name
# root = Tk()
# root.title(root_title)
# frm = ttk.Frame(root, padding=10)
# frm.grid()

# #ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# # GUI Frames
# right_frm = ttk.Frame(frm)
# top_frm = ttk.Frame(frm)
# bottom_frm = ttk.Frame(frm)

# ## Configuring proportions
# root.grid_rowconfigure(1, weight=1)
# root.grid_columnconfigure(1, weight=2)

# right_frm.grid(column=1, columnspan=2, sticky="e")
# top_frm.grid(column=0, row=0, sticky="ne")
# bottom_frm.grid(column=0,row=1, sticky="s")


# # Settings Widgets
# settings_label = ttk.Label(right_frm, text="Settings").grid(row=0, column=0 ,columnspan=2, sticky="n")

# seed_label = ttk.Label(right_frm, text="Seed:").grid(row=1, column=0, sticky="e")
# seed_entry = ttk.Entry(right_frm).grid(row=1, column=1, sticky="w")

# small_button = ttk.Button(right_frm, text="small").grid(row=2, column=0)
# medium_button = ttk.Button(right_frm, text="medium").grid(row=2, column=1)
# large_button = ttk.Button(right_frm, text="large").grid(row=2, column=2)

# generate_button = ttk.Button(right_frm, text="Start").grid(row=3, column=1, sticky="s")

# # Generation Widgets
# entryGenerator = ttk.Entry(top_frm, background="pink", width=50).grid()
# LeftButton = ttk.Button(bottom_frm, text = "Left", padding=5).grid(row=0, column=0, sticky="e")
# CentreButton = ttk.Button(bottom_frm, text = "Centre", padding=5).grid(row=0, column=1, sticky="nsew")
# RightButton = ttk.Button(bottom_frm, text = "Right", padding=5).grid(row=0, column=2, sticky="w")

# label1 = ttk.Label(top_frm, text = "1")

# ~~ 3D grid world generated ~~


class World():

    def __init__(self):
        self.grid_size = 20
        self.maxLayers = 1
        self.world_grid = []
        self.type_emptycell = 1 ### DEBUGGING

    # Generates an 3D list based on variables given
    def initialiseGrid(self):
        # initialise temporary variables
        layerNo = 0
        rowNo = 0
        columnNo = 0 

        for layer in range(0, self.maxLayers):
            rowNo = 0 # resets every new layer
            self.world_grid.append([])

            for row in range(0, self.grid_size):
                self.world_grid[layerNo].append([])

                for column in range(0, self.grid_size):
                    self.world_grid[layerNo][rowNo].append(self.type_emptycell)
                    self.type_emptycell += 1 ### DEBUGGING to test what order values are added into the 2D array
                rowNo += 1
            layerNo += 1
        grid_print = True # Enables/Disables printing
        gen_count = 0

    # ~~ Outputs the Grid ~~
    def outputGrid(self):
        grid_print = True
        while(grid_print):
            layer_input = int(input(f"What layer would you like to see? [1 to {self.maxLayers}]: "))
            layer_print = self.world_grid[layer_input-1]
            for z in layer_print: # Should be printing the rows...
                print(z, end='\n')
            grid_print = False # Concluded and so it will stop
    
    # ~~ Generate noise heigh map ~~
    # Because this is a height map I do not need to create a 3D map. It will just superimpose onto the 3D map.
    def generateNoiseHeight(self):
        hashy = "TempVariableValue"
        hexseedy = md5(str.encode(hashy)).hexdigest()[:16] # Digest is used to return the value of the hash, the square brackets are to truncate this to a smaller size.
        seedy = int(hexseedy, 16) # Turns this hexadecimal string back into base 10.

        noise1 = PerlinNoise(octaves=1, seed=seedy)
        noise2 = PerlinNoise(octaves=3, seed=seedy)
        noise3 = PerlinNoise(octaves=6, seed=seedy)
        noise4 = PerlinNoise(octaves=12, seed=seedy)  # Creates multiple noises to then be combined into 1 height map

        heightmap = []

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                noise_val = noise1([i/self.grid_size, j/self.grid_size])
                noise_val += 0.5 * noise2([i/self.grid_size, j/self.grid_size])
                noise_val += 0.25 * noise3([i/self.grid_size, j/self.grid_size])
                noise_val += 0.125 * noise4([i/self.grid_size, j/self.grid_size])

                row.append(noise_val) # appends each value assigned to a column
            heightmap.append(row) # appends each row into a 2D list

        # ~~Quantising the map~~

        highest_height = 0
        lowest_height = 0
        xvalue = 0
        zvalue = 0
        high_pos = []
        
        zNo = 0
        for z in heightmap:
            for x in z:
                xNo = 0
                if x > highest_height:
                    highest_height = x
                    xvalue = xNo
                    zvalue = zNo
                elif x < lowest_height:
                    lowest_height = x
                else:
                    continue
                xNo += 1
            zNo += 1 

        high_pos = [zvalue, xvalue]
        print(f"Highest = {highest_height} and the lowest = {lowest_height}.... Pos = {high_pos}")





        return heightmap

    def outputHeight(self):
        grid_print = True
        heightmap = self.generateNoiseHeight()
        while(grid_print):
            for x in heightmap: # Should be printing the rows...
                print(x, end='\n')
            grid_print = False # Concluded and so it will stop

#root.mainloop()
Mappy = World()
Mappy.initialiseGrid()
Mappy.outputHeight()
### TESTING TO UNDERSTAND HOW GITHUB WORKS