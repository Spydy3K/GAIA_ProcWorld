from hashlib import md5
from typing import Self
from perlin_noise import PerlinNoise

class World():

    def __init__(self):
        self.grid_size = 20
        self.maxLayers = 10
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
    
    # ~~ Generate noise heigh map ~~
    # Because this is a height map I do not need to create a 3D map. It will just superimpose onto the 3D map.
    def generateNoiseHeight(self, seedy):
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
        #print(half_layer)
        for increment in range(0, self.maxLayers):
            temp_quant = increment - half_layer # effectively the same as (-5 + 1) if you (me) are confused
            self.quants.append(temp_quant)

        #print(f"quant boundaries: {self.quants}")

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

        #print(partion)
        #print(boundaries)
        
        # Simplifying the data finally
        boundary_max = len(boundaries)

        for row in heightmap:

            for column in row:

                for boundary in range(0, boundary_max):
                    limit = boundaries[boundary]

                    if column > limit:
                        heightmap[row][column] = self.quants[boundary]
                    if column == lowest_height:
                        heightmap[row][column] = self.quants[0]
        return heightmap

    def terrainPass(self, seedyVar):

        heightMap = self.generateNoiseHeight(seedyVar)

        # type_sea = 0
        # type_land = 1
        # type_air = 2

        #type_tile = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        print(heightMap)
        print(self.quants)
        for layer in range(0, self.maxLayers): # checking each layer on the y axis

            for row in range(0, self.grid_size): # checking each item on the z axis

                for column in range(0, self.grid_size): # checking each item on the x axis of the initialised grid.
                    #print(f"Coords: {column}, {row}, Layer: {layer} ")
                    tmpVal = heightMap[row][column]

                    if (layer < 4) and (5 - abs(tmpVal)) == layer:
                        if (layer == 0):
                            self.world_grid[layer][row][column] = 5
                        else:
                            self.world_grid[layer][row][column] = 5 - abs(tmpVal)
                    elif (layer < 4) and ((5 - abs(tmpVal)) < layer):
                        self.world_grid[layer][row][column] = 5
                    elif (layer < 4) and ((5 - abs(tmpVal)) > layer):
                        self.world_grid[layer][row][column] = 5

                    elif (layer > 5) and ((5 + abs(tmpVal)) == layer):
                        self.world_grid[layer][row][column] = 5 + abs(tmpVal)
                    elif (layer > 5) and ((5 + abs(tmpVal)) < layer):
                        self.world_grid[layer][row][column] = 9
                    elif (layer > 5) and ((5 + abs(tmpVal)) > layer):
                        self.world_grid[layer][row][column] = 0

                    # if (layer < 4) and ((5 - abs(heightMap[layer])) == layer): # Only for sea values (below -4 on the map) and on the right layer
                    #     if (layer < 4) and (layer == 0): # exception for layer 0
                    #         self.world_grid[layer][row][column] = 5
                    #         print(self.world_grid[layer][row][column])
                    #     else:
                    #         self.world_grid[layer][row][column] = 5 - abs(heightMap[row][column])
                    # elif (layer < 4) and ((5 - abs(self.quants[layer]) > layer)): # Only for sea values and there is a sea above but not below
                    #     self.world_grid[layer][row][column] = 5


                    # elif (layer > 5) and ((5 + self.quants[layer]) == layer): # Above sea and right layer
                    #     self.world_grid[layer][row][column] = 0 + layer
                    # elif (layer > 5) and ((5 + self.quants[layer]) < layer): # Above sea and there is land no land above
                    #     self.world_grid[layer][row][column] = 9
                    # elif (layer > 5) and ((5 + self.quants[layer]) > layer): # Above the sea and there is land above
                    #     self.world_grid[layer][row][column] = 0



    def initiateGeneration(self, seedyVar):

        seedy = seedyVar.get()
        seedy = seedy.strip()

        self.initialiseGrid()
        self.terrainPass(seedy)
        #print(self.world_grid[4])
        return self.world_grid


    def outputHeight(self):
        grid_print = True
        heightmap = self.generateNoiseHeight()
        while(grid_print):
            for x in heightmap: # Should be printing the rows...
                print(x, end='\n')
            grid_print = False # Concluded and so it will stop

# map = World()
# map.initiateGeneration("123ABC")