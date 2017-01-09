appname = 'PyMailGUI 3.0'
saveMailSeparator = 'PyMailGUI' + ('-'*60) + 'PyMailGUI\n'
openSaveFiles = {}

import sys, os, email.utils, email.message, webbrowser, mimetypes
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog import SaveAs, Open, Directory
from tkinter.messagebox import showinfo, showerror, askyesno

from PP4E.Gui.Tools 		import windows
from PP4E.Gui.Tools 		import threadtools
from PP4E.Internet.Email 	import mailtools
from PP4E.Gui.TextEditor	import textEditor

import mailconfig
import popuputils
import wraplines
import messagecache
import html2text
import PyMailGuiHelp

def printStack(exc_info):
	print(exc_info[0])
	print(exc_info[1])
	try:
		traceback.print_tb(exc_info[2], file=sys.stdout)
	except:
		log = open('_pymailerrlog.txt','a')
		log.write('-'*80)
		traceback.print_tb(exc_info[2], file=log)

loadingHdrsBusy = threadtools.ThreadCounter()
deletingBusy 	= threadtools.ThreadCounter()
loadingMsgsBusy = threadtools.ThreadCounter()
sendingBusy		= threadtools.ThreadCounter()
