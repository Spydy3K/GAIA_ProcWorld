class Tileset():
    def __init__(self, tilesize):
        self.xpos = 0
        self.ypos = 0
        self.side = tilesize
        self.layer = 4
        self.mapgenerated = []

    def changeSize(self, option):
        self.side = option
        print(f'Pixel size: {option}')

    def layerChange(self, choice):
        if (self.layer <= 9 and self.layer >= 0):
            if choice == "Down" and self.layer != 0:
                self.layer = self.layer - 1
            elif choice == "Up" and self.layer != 9:
                self.layer = self.layer + 1
        else:
            pass
    
    def populate(self):
        self
        self.xpos = 0
        self.ypos = 0
        limit = 500 // self.side
        tmp_xpos = self.xpos
        tmp_ypos = self.ypos
        tilelist = []

        for column in range(0, limit):
            self.xpos = 0
            tmp_ypos = self.ypos + self.side

            for row in range(0, limit):

                tmp_xpos = self.xpos + self.side
                tilelist.append([tmp_xpos, tmp_ypos])
                self.xpos = tmp_xpos

            self.ypos = tmp_ypos

        return tilelist

    def drawTiles(self, map, canvas):

        tilelist = self.populate()
        mapgrid = map[self.layer]
        
        xpos = 0
        ypos = 0
        tmp_ypos = 0
        tmp_xpos = 0

        colour = ["lightcyan2", "navy", "dodgerblue4", "dodgerblue3", "deepskyblue3", "khaki", "green3", "springgreen4", "darkgoldenrod3", "slategray"]

        tmp_ycoord = 0

        xcount = -1
        zcount = -1
        colour_choice = 0
        for coords in tilelist:

            #print(f'The tile coords are: ({coords[0]}, {coords[1]})') # testing prints
            #print(f'The previous coords are: ({xpos}, {ypos})')
            
            if coords[0] != self.side:
                tmp_xpos = coords[0]
                tmp_ypos = coords[1]
                xcount += 1
            else:
                xpos = 0
                tmp_xpos = coords[0]
                ypos = tmp_ycoord
                tmp_ypos = coords[1]
                zcount += 1
                xcount = 0
                
            tmp_ycoord = coords[1]
            #print(f'The X and Z count: {xcount}, {zcount}')
            colour_choice = mapgrid[zcount][xcount]
            canvas.create_rectangle(xpos, ypos, tmp_xpos, tmp_ypos, fill=colour[colour_choice], width=0)
            xpos = tmp_xpos
        
        print(f'CURRENT LAYER: {self.layer}')
        print("~~~")

    
#test = Tileset(5)
#print(test.populate())







        