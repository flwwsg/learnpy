#!/usr/bin/python3
from tkinter import *
from launchmodes import PortableLauncher

demoModules = ['demoDlg', 'demoRadio', 'demoCheck', 'demoScale']

for demo in demoModules:
	PortableLauncher(demo, demo+'.py')()

root = Tk()
root.title('Processes')
Label(root, text='Multiple Toplevel window demo: command lines', bg='white').pack()
root.mainloop()
