#!/usr/bin/env python
import Tkinter as tk
import sys
from functools import partial

class App:


    def __init__(self, master, rows, columns):		

        self.turn = 'player1'
        
        for row in rows:
            setattr(self, row, tk.Frame(master))  # Each row is a frame, which will be stacked with 1,..,n buttons from left to right
            current_row = getattr(self, row)
            current_row.pack(side=tk.TOP)
            for column in columns:
                setattr(self, row + column, tk.Button(current_row,height=5,width=5,font = ("Times", 20, "bold")))
                current_button = getattr(self, row + column)
                # The bit below is tricky.  If you say something like 'command = function(argument)', that's actually a call to that function.
                # The usual thing is to do 'command = function', which is a reference to the function itself without calling it, but then
                # you have no arguments.  This is usually (it seems) overcome using lambda functions, but the 'partial' command from functools
                # seems neat.  It returns a reference to a function that behaves like the given function called with the given parameters!
                current_button.configure(command = partial(self.take_turn,current_button,rows,columns))
                current_button.pack(side=tk.LEFT)

    def take_turn(self, current_button, rows, columns):
        if self.turn == 'player1': current_button.configure(text = 'X')
        else: current_button.configure(text = 'O')
        
        # Call a function here to see if the game has been won
        self.check_game_finished(rows, columns)
        self.change_turn()
    
    def change_turn(self):
        if self.turn == 'player1' : self.turn = 'player2'
        else: self.turn = 'player1'
        
    def check_game_finished(self, rows, columns):
        possible_wins = []
        # Here I'm making a list of all the rows, columns and diagonals.
        # Each entry in the list will be a list of the buttons in that row / column / diagonal
        # I then check to see if each button in any entry is all Xs or all Os
        # If they are, the game is won and I change their colour
        
        # Bit of a faff - I have to add all the rows, columns and diagonals to the list and am not sure of a quick easy way to do it!
        # Add rows to possible wins
        for row in rows:
            possible_win = []
            for column in columns:
                possible_win.append(getattr(self, row + column))
            possible_wins.append(possible_win)
        # Add columns to possible wins
        for column in columns:
            possible_win = []
            for row in rows:
                possible_win.append(getattr(self, row + column))
            possible_wins.append(possible_win)
        # Add two diagonals to possible wins
        possible_win = []
        for (row, column) in zip(rows, columns):
            possible_win.append(getattr(self, row + column))
        possible_wins.append(possible_win)
        possible_win = []
        rows_reversed = rows
        rows_reversed.reverse()
        for (row, column) in zip(rows_reversed, columns):
            possible_win.append(getattr(self, row + column))
        possible_wins.append(possible_win)
        
        player1_win = [ 'X' for i in range(0,len(rows)) ]
        player2_win = ['O' for i in range(0,len(rows)) ]
        winners = [ player1_win, player2_win ]
        
        # Is there any row, column or diagonal that is all Xs or all Os (ie. the two entries in the 'winners' list)?
        # If so, change the colour of those buttons to signal end of game!
        for line in possible_wins:
            if [ line[i].cget('text') for i in range(0,len(line)) ] in winners:
                print "We have a winner!"
                for i in range(0, len(line)):
                    line[i].configure(bg='green',fg='blue')


def main():
    root = tk.Tk()
    
    # This should be run with a number n as the first argument.
    # This sets up an n * n grid to play on.
    try:
        size = int(sys.argv[1])
        # We label the rows r0, r2, ..., rn-1
        rows = [ 'r' + str(i) for i in range(0, size) ]
    except:
        sys.exit('First argument should be size of grid')
    # We similarly label the columns c0, ..., cn-1  
    columns = [ 'b' + entry.lstrip('r') for entry in rows ]
    
    
    App(root, rows, columns)

    root.mainloop()
    return

if __name__ == "__main__":
    main()