from tkinter import *
import os

entrysize = 40

# labels = [('label':label, 'button':button, 'command':command),()]
class Form:
	def __init__(self, labels, parent):
		self.parent = parent
		labelsize = max(len(x[0]) for x in labels) + 2
		box = Frame(parent)
		box.pack(expand=YES, fill=X)
		rows = Frame(box, bd=2, relief=GROOVE)
		rows.pack(side=TOP, expand=YES, fill=X)
		self.content = {}
		for item in labels:
			var = StringVar()
			label = item[0]
			button = item[1]
			command = item[2]
			row = Frame(rows)
			row.pack(fill=X)
			Label(row, text=label, width=labelsize).pack(side=LEFT)
			entry = Entry(row, width=entrysize, textvariable=var)
			entry.pack(side=LEFT, expand=YES, fill=X)
			if button:
				btn = command(var, button, row)
			self.content[label] = entry
		box.master.bind('<Return>', lambda event: self.onSubmit())

	def onSubmit(self):
		pass

	def onCancel(self):
		self.parent.quit()

class FileDlg(Form):
	def __init__(self, labels, parent):
		Form.__init__(self, labels, parent)
		self.root = parent
		self.labels = labels

	def onSubmit(self):
		for item in self.labels:
			label = item[0]
			button = item[1]
			if not button:
				fname = self.content[label].get()
			else:
				fpath = self.content[label].get()
				fpath = os.path.abspath(fpath)

		return fname, fpath
		
		# AddEntry(fname, fname, fpath, self.root )

		# with open(self.config, 'a', encoding='utf-8') as fs:
		# 	fs.write('\n'+fname+'='+fpath)
		# self.onCancel()
		
