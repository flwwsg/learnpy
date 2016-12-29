#!/usr/bin/python3
from tkinter import *

class ScrolledList(Frame):
	def __init__(self, options, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.makeWidgets(options)

	def makeWidgets(self, options):
		sbar = Scrollbar(self)
		list = Listbox(self, relief=SUNKEN)
		sbar.config(command=list.yview)
		list.config(yscrollcommand=sbar.set)
		sbar.pack(side=RIGHT, fill=Y)
		list.pack(side=LEFT, expand=YES, fill=BOTH)
		pos = 0
		for label in options:
			list.insert(pos, label)
			pos += 1
		self.listbox = list

		