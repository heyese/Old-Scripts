#!/usr/bin/env python
import Tkinter as tk

class App:

    def __init__(self, master):

        frame1 = tk.Frame(master)
        frame1.pack(side=tk.TOP)
        frame2 = tk.Frame(master)
        frame2.pack(side=tk.TOP)
        #frame3 = tk.Frame(master)
        #frame3.pack(side=tk.TOP)		

        self.f1b1 = tk.Button(frame1,height=10,width=10,bg="black",command=self.change_colour)
        self.f1b1.pack(side=tk.LEFT)
        self.f1b2 = tk.Button(frame1,height=10,width=10)
        self.f1b2.pack(side=tk.LEFT)
        self.f1b3 = tk.Button(frame1,height=10,width=10)
        self.f1b3.pack(side=tk.LEFT)		

        self.f2b1 = tk.Button(frame2,height=10,width=10)
        self.f2b1.pack(side=tk.LEFT)
        self.f2b2 = tk.Button(frame2,height=10,width=10)
        self.f2b2.pack(side=tk.LEFT)
        self.f2b3 = tk.Button(frame2,height=10,width=10)
        self.f2b3.pack(side=tk.LEFT)

    def change_colour(self):
        print "bg is set to : ", self.f1b1.bg
        self.f1b1.configure(bg="white")

root = tk.Tk()

app = App(root)

root.mainloop()