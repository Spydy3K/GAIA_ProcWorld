from os import path
from hashlib import md5
from typing import Self
from perlin_noise import PerlinNoise

class World():

    def __init__(self):
        self.grid_size = 100
        self.maxLayers = 10
        self.world_grid = []
        self.type_emptycell = 1 ### DEBUGGING
        self.seed = ""
        self.status = False
        self.files = [["Saves/SaveFile1.txt", 0], ["Saves/SaveFile2.txt", 0], ["Saves/SaveFile3.txt", 0], ["Saves/SaveFile4.txt", 0], ["Saves/SaveFile5.txt", 0]]
        for file in self.files:
            tmpFile = open(file[0], "r")
            tmpFile.seek(0, 2)
            if tmpFile.tell() != 0:
                file[1] = 1
            tmpFile.close()
    def changeSize(self, option):
        match option:
            case "Small":
                self.grid_size = 100
                print("100x100")
            case "Medium":
                self.grid_size = 250
                print("250x250")
            case "Large":
                self.grid_size = 500
                print("500x500")

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


    # ~~ Generate noise heigh map ~~
    # Because this is a height map I do not need to create a 3D map. It will just superimpose onto the 3D map.
    def generateNoiseHeight(self, seedy):
        self.seed = seedy
        hashy = seedy
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

        for increment in range(0, (self.maxLayers)):
                temp_quant = increment - half_layer # effectively the same as (-5 + 1) if you (me) are confused
                self.quants.append(temp_quant)
        for x in range(half_layer, self.maxLayers):
            self.quants[x] += 1

        #print(f"quant boundaries: {self.quants}")

        for z in heightmap:
            for x in z:
                if x > highest_height:
                    highest_height = x
                elif x < lowest_height:
                    lowest_height = x
                else:
                    continue

        #print(f"Highest = {highest_height} and the lowest = {lowest_height}....")

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

        # Simplifying the data
        boundary_max = len(boundaries)
        z = 0
        for row in heightmap:
            x = 0
            for column in row:

                for boundary in range(0, boundary_max):
                    limit = boundaries[boundary]

                    if column > limit:
                        heightmap[z][x] = self.quants[boundary]
                    if column == lowest_height:
                        heightmap[z][x] = self.quants[0]

                x += 1
            z += 1

        return heightmap

    def terrainPass(self, seedyVar):

        heightMap = self.generateNoiseHeight(seedyVar)
        #print(heightMap[55][92])
        for layer in range(0, self.maxLayers): # checking each layer on the y axis

            for row in range(0, self.grid_size): # checking each item on the z axis

                for column in range(0, self.grid_size): # checking each item on the x axis of the initialised grid.
                    #print(f"Coords: {column}, {row}, Layer: {layer} ")
                    tmpVal = heightMap[row][column]
                    
                    if (layer <= 4) and (tmpVal < 1): # If its sealvl and NOT land
                        if (layer >= 5 + tmpVal):
                            self.world_grid[layer][row][column] = 5 + tmpVal
                        elif (layer < 5 + tmpVal):
                            self.world_grid[layer][row][column] = 5
                        if (tmpVal == -5):
                            if layer == 0:
                                self.world_grid[layer][row][column] = 5
                            else:
                                self.world_grid[layer][row][column] = 4
                    if (layer <= 4) and (tmpVal >= 1): # If its sea level and IS land
                        if (tmpVal == 1):
                            self.world_grid[layer][row][column] = 5
                        else:
                            self.world_grid[layer][row][column] = 9

                    if (layer > 4) and (tmpVal > 1): # If it is above sealvl and not sand
                        if (layer == 3 + tmpVal): # if the right layer
                            self.world_grid[layer][row][column] = 4 + tmpVal
                        elif (layer < 3 + tmpVal): # if larger than the layer
                            self.world_grid[layer][row][column] = 9
                        else: # if less than the layer
                            self.world_grid[layer][row][column] = 0
                    if (layer > 4) and (tmpVal <= 1): # if its 1
                        self.world_grid[layer][row][column] = 0

    ### Self.status shenanigans
    def initiateGeneration(self, seedyVar):
        if self.status != True:
            seedy = seedyVar.get()
            seedy = seedy.strip()
            self.initialiseGrid()
            self.terrainPass(seedy)
            return self.world_grid
        else:
            seedy = self.seed
            self.initialiseGrid()
            self.terrainPass(seedy)
            return self.world_grid


    def outputHeight(self):
        grid_print = True
        heightmap = self.generateNoiseHeight()
        while(grid_print):
            for x in heightmap: # Should be printing the rows...
                print(x, end='\n')
            grid_print = False # Concluded and so it will stop

    # Checks all the saves empty or not


    def exportWorld(self):
        savable = []
        print("""
                Saves available to Save To
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """)
        for file in self.files:
            if file[1] == 0:
                savable.append(file[0])
                print(f"{file[0]}")
        userinput = int(input(f"Which file to Save to? {savable} or -1 to cancel")) 
        if userinput == 1:       
            tmpFile = open(savable[userinput-1], "w+")
            tmp = self.seed
            tmpFile.write(tmp)
            tmpFile.close()
            file[1] = 1
            print("Exported.")
            print("~~~~~~~~~~")
    
    def importWorld(self):
        loadable = []
        print("""
                Saves available to Load From
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """)
        for file in self.files:
            if file[1] == 1:
                loadable.append(file[0])
                print(f"{file[0]}")
        userinput = int(input(f"Which file to load? {loadable} or -1 to cancel"))

        if userinput != -1:
            tmpFile = open(loadable[userinput-1], "r")
            seed = tmpFile.read()
            tmpFile.close()
            print("Imported.")
            print("~~~~~~~~~~")
            return seed
    
    def resetSaves(self):
        for file in self.files:
            tmpFile = open(file[0], "w")
            tmpFile.close()
            file[1] = 0
            print("Cleared.")