'''config-label.py'''
from tkinter import *
root = Tk()
labelfont = ('times',20,'bold')
widget = Label(root, text='Hello config world')
widget.config(bg='black', fg='yellow')
widget.config(font=labelfont)
widget.pack(expand=YES, fill=BOTH)
root.mainloop()