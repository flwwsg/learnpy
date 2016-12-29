#!/usr/bin/python3

from tkinter.messagebox import showinfo

class LauncherExcept(Except):
	def __init__(self, title, info):
		self.title = title
		self.info = info

	def info(self):
		showinfo(self.title, self.info)