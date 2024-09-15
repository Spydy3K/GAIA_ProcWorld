from tkinter import *
from tkinter import ttk

# ~~ Window generated ~~
#root_title = 'GAIA' # Variable for the window name
#root = Tk()
#root.title(root_title)
#frm = ttk.Frame(root, padding=10)
#frm.grid()
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# ~~ Grid generated ~~
grid_size = 100
world_grid = [] # Using an array because it is simple. Temp?
# type_emptycell = '[]'
type_emptycell = 1 ### DEBUGGING
rowNo = 0

# Generates a list based on variables given

for row in range(0, grid_size):
    world_grid.append([])
    for column in range(0, grid_size):
        world_grid[rowNo].append(type_emptycell)
        type_emptycell += 1 ### DEBUGGING to test what order values are added into the 2D array
    rowNo += 1

grid_print = True # Enables/Disables printing
gen_count = 0

while(grid_print):
    for y in world_grid: # Should be printing the rows...
        print(y, end='\n')
    grid_print = False # Concluded and so it will stop

#root.mainloop()