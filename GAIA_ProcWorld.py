from tkinter import *
from tkinter import ttk

from hashlib import md5
from typing import Self
from perlin_noise import PerlinNoise

from math import trunc


# ~~ 3D grid world generated ~~


class World():

    def __init__(self):
        self.grid_size = 10
        self.maxLayers = 5
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

        # ~~Quantsizing the map~~

        highest_height = 0
        lowest_height = 0

        self.quants = [] # generate the values that determine if its below or above sea level

        half_layer = self.maxLayers // 2 
        temp_quant = 0
        print(half_layer)
        for increment in range(0, self.maxLayers):
            temp_quant = increment - half_layer # effectively the same as (-5 + 1) if you (me) are confused
            self.quants.append(temp_quant)

        print(f"quant boundaries: {self.quants}")

        for z in heightmap:
            for x in z:
                if x > highest_height:
                    highest_height = x
                elif x < lowest_height:
                    lowest_height = x
                else:
                    continue

        print(f"Highest = {highest_height} and the lowest = {lowest_height}....")

        # Creating the boundaries of the quantised map according to the 3D array
        diff = abs(highest_height - lowest_height) # to make sure the difference is a positive number
        partion = diff / self.maxLayers
        partion = round(partion, 8) # rounding to 8 decimal place instead of automatic 17 because of floating point arithmetic being wack or me being stupid

        boundaries = []
        height_increase = 0
        temp_height = round(lowest_height, 8)

        for boundary in range(0, self.maxLayers):
            height_increase = partion * boundary
            temp_height = temp_height + height_increase
            temp_height = round(temp_height, 8)
            boundaries.append(temp_height)
            temp_height = lowest_height # This resets it back to the lowest to then be added onto

        print(partion)
        print(boundaries)
        
        # Simplifying the data finally
        boundary_max = len(boundaries)
        rowNo = 0
        for row in heightmap:
            columnNo = 0
            for column in row:

                for boundary in range(0, boundary_max):
                    limit = boundaries[boundary]

                    if column > limit:
                        heightmap[rowNo][columnNo] = self.quants[boundary]
                    else:
                        continue
                columnNo +=1
            rowNo += 1


        return heightmap

    def terrainPass(self):

        terrainMap = self.generateNoiseHeight()

        type_sea = -1
        type_land = 0
        type_air = 1

        layerNo = 0
        print(self.quants)
        for layer in range(0, self.maxLayers):
            rowNo = 0 # resets every new layer

            for row in range(0, self.grid_size):

                for column in range(0, self.grid_size): # checking each column of the initialised grid.

                    if self.quants[layerNo] < 0:
                        if (terrainMap[rowNo][column] < self.quants[layerNo]) and (terrainMap[rowNo][column] < 0): # if the noise says it is less than the layer and the layer is below zero than it is land
                            self.world_grid[layerNo][rowNo][column] = type_sea
                        elif (terrainMap[rowNo][column] > self.quants[layerNo]) and (terrainMap[rowNo][column] < 0): # if the noise says it is more than the layer and the layer is more than or equal to zero than it is sea
                            self.world_grid[layerNo][rowNo][column] = type_land
                        elif (terrainMap[rowNo][column] == self.quants[layerNo]) and (terrainMap[rowNo][column] < 0): 
                            self.world_grid[layerNo][rowNo][column] = type_sea
                        elif (terrainMap[rowNo][column] > self.quants[layerNo]) and (terrainMap[rowNo][column] >= 0): 
                            self.world_grid[layerNo][rowNo][column] = type_land
                    else:
                        if (terrainMap[rowNo][column] < self.quants[layerNo]) and (terrainMap[rowNo][column] < 0):
                            self.world_grid[layerNo][rowNo][column] = type_air
                        elif (terrainMap[rowNo][column] > self.quants[layerNo]):
                            self.world_grid[layerNo][rowNo][column] = type_land
                        elif (terrainMap[rowNo][column] == self.quants[layerNo]):
                            self.world_grid[layerNo][rowNo][column] = type_land
                        elif (terrainMap[rowNo][column] < self.quants[layerNo]) and (terrainMap[rowNo][column] >= 0):
                            self.world_grid[layerNo][rowNo][column] = type_air


                rowNo += 1

            layerNo += 1


    def outputHeight(self):
        grid_print = True
        heightmap = self.generateNoiseHeight()
        while(grid_print):
            for x in heightmap: # Should be printing the rows...
                print(x, end='\n')
            grid_print = False # Concluded and so it will stop

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

root.mainloop()

### TESTING TO UNDERSTAND HOW GITHUB WORKS