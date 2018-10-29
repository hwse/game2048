import tkinter
from tkinter import messagebox
import logging

LOGGER = logging.getLogger(__name__)

class GUI():

    def __init__(self, game_state):
        self.game_state = game_state
        
        self.root = tkinter.Tk()
        self.root.title('2048')
        self.frame = tkinter.Frame(self.root)

        # create the label grid
        self.rows = []
        for y in range(game_state.WIDTH):
            label_row = []
            for x in range(game_state.HEIGHT):
                label = tkinter.Label(width=10, height=5, relief=tkinter.RIDGE)
                label.grid(row=y, column=x)
                label_row.append(label)
            self.rows.append(label_row)

        # register key input
        self.root.bind('<Up>', self.key_callback)
        self.root.bind('<Right>', self.key_callback)
        self.root.bind('<Down>', self.key_callback)
        self.root.bind('<Left>', self.key_callback)

    def key_callback(self, event):
        LOGGER.info('key pressed: {}'.format(event.keysym))
        lost = self.game_state.handle_key(event.keysym)
        self.set_labels(self.game_state.game_grid)
        if lost:
            messagebox.showinfo(title='INFO', message='you lost')
            self.root.destroy()
        
    def set_labels(self, game_grid):
        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                nr = game_grid[x][y]
                txt = str(nr) if nr is not None else ''
                color = '#60FF00' if nr is not None else '#000000'
                cell.configure(text=txt, bg=color)
    
    def run(self):
        self.set_labels(self.game_state.game_grid)
        self.root.mainloop()
