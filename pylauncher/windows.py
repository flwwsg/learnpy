import os, glob
from tkinter import Tk, Toplevel, Frame, YES, BOTH, RIDGE
from tkinter.messagebox import showinfo, askyesno

class MainWindow(Tk):
	def __init__(self, app):
		Tk.__init__(self)
		self.__app = app
		self.title(app)

	def quit(self):
		if self.okayToQuit():
			if askyesno(self.__app, 'Quit?'):
				self.destroy()
		else:
			showinfo(self.__app, 'Quit not allowed')

	def destroy(self):
		Tk.quit(self)

	def okayToQuit(self):
		return True

class PopupWindow(Toplevel):
	def __init__(self, app):
		Toplevel.__init__(self)
		self.__app = app
		self.title(app)

	def quit(self):
		if askyesno(self.__app, 'Quit?'):
			self.destroy()

	def destroy(self):
		Toplevel.destroy(self)


class QuietPopuWindow(PopupWindow):
	def quit(self):
		self.destroy()

class ComponentWindow(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.config(relief=RIDGE, border=2)

	def quit(self):
		showinfo('Quit', 'Not supported in attachment mode')