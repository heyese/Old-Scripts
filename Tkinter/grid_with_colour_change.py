#!/usr/bin/env python
import Tkinter as tk
from functools import partial

class App:

    def __init__(self, master):		

        rows = ['r1', 'r2', 'r3']
        buttons = ['b1', 'b2', 'b3']
        
        for row in rows:
            setattr(self, row, tk.Frame(master))
            current_row = getattr(self, row)
            current_row.pack(side=tk.TOP)
            for button in buttons:
                setattr(self, row + button, tk.Button(current_row,height=10,width=10,bg='white'))
                current_button = getattr(self, row + button)
                # The bit below is tricky.  If you say something like 'command = function(argument)', that's actually a call to that function.
                # The usual thing is to do 'command = function', which is a reference to the function itself without calling it, but then
                # you have no arguments.  This is usually (it seems) overcome using lambda functions, but the partial command from functools
                # seems neat.  It returns a reference to a function that behaves like the given function called with the given parameters!
                current_button.configure(command = partial(self.change_colour,current_button))
                current_button.pack(side=tk.LEFT)

    def change_colour(self, current_button):
        colour = current_button.cget('bg')
        print "Colour is ", colour
        if colour == 'white':
            current_button.configure(bg = 'black')
        else:
            current_button.configure(bg = 'white')
        #print "bg is set to : ", self.f1b1.bg
        #self.f1b1.configure(bg="white")
        
root = tk.Tk()

app = App(root)

root.mainloop()