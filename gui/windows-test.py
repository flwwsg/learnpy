'''windows-test.py'''

from tkinter import Button, mainloop
from windows import MainWindow, PopuWindow, ComponentWindow

def _selftest():
	
	class content:
		def __init__(self):
			Button(self, text='Larch', command=self.quit).pack()
			Button(self, text='Sing', command=self.destroy).pack()

	class contentmix(MainWindow, content):
		def __init__(self):
			MainWindow.__init__(self, 'mixin', 'Main')
			content.__init__(self)

	contentmix()

	class contentmix(PopuWindow, content):
		def __init__(self):
			PopuWindow.__init__(self, 'mixin', 'Popup')
			content.__init__(self)

	prev = contentmix()

	class contentmix(ComponentWindow, content):
		def __init__(self):
			ComponentWindow.__init__(self, prev)
			content.__init__(self)

	contentmix()

	class contentsub(PopuWindow):
		def __init__(self):
			PopuWindow.__init__(self, 'popup', 'subclass')

			Button(self, text='Pine', command=self.quit).pack()
			Button(self, text='Sing', command=self.destroy).pack()

	contentsub()

	win = PopuWindow('popup', 'attachment')
	Button(win, text='Redwood', command=win.quit).pack()
	Button(win, text='Sing', command=win.destroy).pack()
	mainloop()

if __name__ == '__main__':
	_selftest()
			

			