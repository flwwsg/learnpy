'''mainloopdemo.py'''
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Demo(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		Label(self, text='Basic demos').pack()
		Button(self, text='open', command=self.openfile).pack(fill=BOTH)
		Button(self, text='save', command=self.savefile).pack(fill=BOTH)
		self.open_name = self.save_name = ''

	def openfile(self):
		self.open_name = askopenfilename()

	def savefile(self):
		self.save_name = asksaveasfilename(initialdir=r'd:\dev')

if __name__ == '__main__':
	print('popup1...')
	mydialog = Demo()
	mydialog.mainloop()

	print(mydialog.open_name)
	print(mydialog.save_name)

	print('popup2...')
	mydialog = Demo()
	mydialog.mainloop()
	print(mydialog.open_name)
	print(mydialog.save_name)
	print('ending...')
	