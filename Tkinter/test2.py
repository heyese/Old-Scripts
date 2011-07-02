#!/usr/bin/env python
import Tkinter as tk
from functools import partial

class App:


    def __init__(self, master, rows, buttons):		

        self.turn = 'player1'
        
        for row in rows:
            setattr(self, row, tk.Frame(master))
            current_row = getattr(self, row)
            current_row.pack(side=tk.TOP)
            for button in buttons:
                setattr(self, row + button, tk.Button(current_row,height=5,width=5,font = ("Times", 20, "bold")))
                current_button = getattr(self, row + button)
                # The bit below is tricky.  If you say something like 'command = function(argument)', that's actually a call to that function.
                # The usual thing is to do 'command = function', which is a reference to the function itself without calling it, but then
                # you have no arguments.  This is usually (it seems) overcome using lambda functions, but the 'partial' command from functools
                # seems neat.  It returns a reference to a function that behaves like the given function called with the given parameters!
                current_button.configure(command = partial(self.take_turn,current_button))
                current_button.pack(side=tk.LEFT)

    def take_turn(self, current_button):
        if self.turn == 'player1': current_button.configure(text = 'X')
        else: current_button.configure(text = 'O')
        
        # Call a function here to see if the game has been won
        self.check_game_finished(rows, buttons)
        self.change_turn()
    
    def change_turn(self):
        if self.turn == 'player1' : self.turn = 'player2'
        else: self.turn = 'player1'
        
    def check_game_finished(self, rows, buttons):
        possible_wins = []
        # Add rows to possible wins
        for row in rows:
            possible_win = []
            for button in buttons:
                possible_win.append(getattr(self, row + button).cget('text'))
            possible_wins.append(possible_win)
        # Add columns to possible wins
        for button in buttons:
            possible_win = []
            for row in rows:
                possible_win.append(getattr(self, row + button).cget('text'))
            possible_wins.append(possible_win)
        # Add two diagonals to possible wins
        possible_win = []
        for (row, button) in zip(rows, buttons):
            possible_win.append(getattr(self, row + button).cget('text'))
        possible_wins.append(possible_win)
        possible_win = []
        rows_reversed = rows
        rows_reversed.reverse()
        for (row, button) in zip(rows_reversed, buttons):
            possible_win.append(getattr(self, row + button).cget('text'))
        possible_wins.append(possible_win)
        
        if ['X','X','X'] in possible_wins: print "Player1 has won"
        if ['O','O','O'] in possible_wins: print "Player2 has won"

        
root = tk.Tk()
rows = ['r1', 'r2', 'r3']
buttons = ['b1', 'b2', 'b3']
app = App(root, rows, buttons)

root.mainloop()