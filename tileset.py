class Tileset():
    def __init__(self, tilesize):
        self.xpos = 0
        self.ypos = 0
        self.side = tilesize
        self.limit = 500 // tilesize # how many tiles will fit in a 500x500 square

    def populate(self):

        self.xpos = 0
        self.ypos = 0
        limit = self.limit
        tmp_xpos = self.xpos
        tmp_ypos = self.ypos
        tilelist = []

        for column in range(0, limit):
            tmp_ypos = self.ypos + self.side
            self.xpos = 0
            for row in range(0, limit):

                tmp_xpos = self.xpos + self.side
                tilelist.append([tmp_xpos, tmp_ypos])
                self.xpos = tmp_xpos

            self.ypos = tmp_ypos
        
        return tilelist

testing = Tileset(5)
print(testing.populate())




        