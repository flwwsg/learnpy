'''PyGadgets.py'''

import sys, time, os, time
from tkinter import *
from launchmodes import PortableLauncher
from windows import MainWindow

def runImmediate(mytools):
	print('Starting Python/Tk gadgets...')
	for (name, commandLine) in mytools:
		PortableLauncher(name, commandLine)()
	print('One moment please ...')
	if sys.platform[:3] == 'win':
		for i in range(10):
			time.sleep(1)
			print('.' * 5 * (i+1))

def runLauncher(mytools):
	root = MainWindow('PyGadgets PP4E')
	for (name, commandLine) in mytools:
		b = Button(root, text=name, fg='black', bg='beige', border=2,
			command=PortableLauncher(name, commandLine))
		b.pack(side=LEFT, expand=YES, fill=BOTH)

	root.mainloop()

mytools = [
	('PyEdit', 'textEditor.py'),
	('PyCalc', 'calculator.py'),
	('PyMail', 'Internet/PyMailGui.py')
]

if __name__ == '__main__':
	prestart, toolbar = True, False
	if prestart:
		runImmediate(mytools)
	if toolbar:
		runLauncher(mytools)