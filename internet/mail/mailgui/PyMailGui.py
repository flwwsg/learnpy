import mailconfig, sys
from SharedNames import appname, windows
from ListWindows import PyMailServer, PyMailFile

srvname = mailconfig.popservername or 'Server'

class PyMailServerWindow(PyMailServer, windows.MainWindow):
	"""docstring for PyMailServerWindow"""
	def __init__(self):
		windows.MainWindow.__init__(self, appname, srvname)
		PyMailServer.__init__(self)

class PyMailServerPopup(PyMailServer, windows.PopupWindow):
	def __init__(self):
		windows.PopupWindow.__init__(self, appname, srvname)
		PyMailServer.__init__(self)

class PyMailServerComponent(PyMailServer, windows.ComponentWindow):
	def __init__(self):
		windows.ComponentWindow.__init__(self)
		PyMailServer.__init__(self)

class PyMailFileWindow(PyMailFile, windows.PopupWindow):
	def __init__(self, filename):
		windows.PopupWindow.__init__(self, appname, filename)
		PyMailFile.__init__(self, filename)


if __name__ == '__main__':
	rootwin = PyMailServerWindow()
	if len(sys.argv) > 1:
		for savename in sys.argv[1:]:
			rootwin.onOpenMailFile(savename)
		rootwin.lift()
	rootwin.mainloop()

	
		
		
		