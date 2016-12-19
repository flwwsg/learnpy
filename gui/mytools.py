#!/usr/bin/env python3

from shellgui import *
from packdlg import runPackDialog
from unpackdlg import runUnpackDialog

class TextPak1(ListMenuGui):
	def __init__(self):
		self.myMenu = [
			('Pack', runPackDialog),
			('Unpack', runUnpackDialog),
			('Mtool', self.notdone)
		]
		ListMenuGui.__init__(self)

	def forToolBar(self, label):
		return label in {'Pack', 'Unpack'}

class TextPak2(DictMenuGui):
	def __init__(self):
		self.myMenu = {
		'Pack':runPackDialog,
		'Unpack':runUnpackDialog,
		'Mtool':self.notdone
		}
		DictMenuGui.__init__(self)

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1 and argv[1] == 'list':
		print('list test')
		TextPak1().mainloop()
	else:
		print('dict test')
		TextPak2().mainloop()
		
		
		