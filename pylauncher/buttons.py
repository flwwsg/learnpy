from tkinter import *
from tkinter.filedialog import askopenfilename
from launchmodes import QuietPortableLauncher


class CustomBtn(Frame):
	def __init__(self, text, command ,parent=None, sideonparent=TOP):
		rowfrm = Frame(parent)
		rowfrm.pack(side=sideonparent)
		btn = Button(rowfrm,relief=RIDGE, border=4, text=text, width=20,command=command)
		btn.pack(side=LEFT, fill=BOTH, expand=YES)

class Quitter(CustomBtn):
	def __init__(self, parent):
		CustomBtn.__init__(self, 'Quit', parent.quit, parent, sideonparent=TOP)

class NewProgram(CustomBtn):
	def __init__(self, command ,parent=None, sideonparent=TOP):
		CustomBtn.__init__(self, 'new program', command, parent, sideonparent)

class AddEntry(CustomBtn):
	def __init__(self, name, label, doit, parent=None,sideonparent=TOP):
		CustomBtn.__init__(self, name, QuietPortableLauncher(label, doit), parent, sideonparent)

class OpenFile(CustomBtn):
	def __init__(self, var, name='OpenFile', parent=None, sideonparent=RIGHT):
		funct = lambda: var.set(askopenfilename() or var.get())
		CustomBtn.__init__(self, name, funct, parent, sideonparent)