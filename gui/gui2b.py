'''gui2b.py'''
from tkinter import *
import sys
root = Tk()
Button(root, text='press', 
	command=(lambda: print('Hello lambda world') or sys.exit())).pack(side=LEFT, expand=YES, fill=X)
root.mainloop()