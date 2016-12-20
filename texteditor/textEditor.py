#! /usr/bin/env python3
'''textEditor.py'''

Version = '2.1'

import sys, os
from tkinter import *
from tkinter.filedialog import Open, SaveAs
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
from guimaker import *

try:
	import textConfig
	configs = textConfig._dict
except:
	configs = {}

helptext = 'PyEdit %s'

START = '1.0'
SEL_FIRST = SEL + '.first'
SEL_LAST = SEL + '.last'

FontScale = 0
if sys.platform[:3] != 'win':
	FontScale = 3

class TextEditor:
	startfiledir = '.'
	editwindows = []
	if __name__ == '__main__':
		from textConfig import(
			opensAskUser, opnesEncoding, 
			savesUseKnownEncoding, savesAskUser, savesEncoding
			)
	else:
		from .textConfig import(
			opensAskUser, opnesEncoding,
			savesUseKnownEncoding, savesAskUser, savesEncoding
			)

	ftypes = [
			('All files', '*'),
			('Text files', '.txt'),
			('Python files', '.py')
	]
	colors = [
			{'fg':'black', 'bg':'white'},
			{'fg':'yellow', 'bg':'black'},
			{'fg':'white', 'bg':'blue'},
			{'fg':'black', 'bg':'beige'},
			{'fg':'yellow', 'bg':'purple'},
			{'fg':'black', 'bg':'brown'},
			{'fg':'lightgreen', 'bg':'darkgreen'},
			{'fg':'darkblue', 'bg':'orange'},
			{'fg':'orange', 'bg':'darkblue'}
	]

	fonts = [
			('courier', 9+FontScale, 'normal'),
			('courier', 12+FontScale, 'normal'),
			('courier', 10+FontScale, 'bold'),
			('courier', 10+FontScale, 'italic'),
			('times', 10+FontScale, 'normal'),
			('helvetica', 10+FontScale, 'normal'),
			('ariel', 10+FontScale, 'normal'),
			('system', 10+FontScale, 'normal'),
			('courier', 20+FontScale, 'normal')
	]
	def __init__(self, loadFirst='', loadEncode=''):
		if not isinstance(self, GuiMaker):
			raise TypeError('TextEditor needs GuiMaker mixin')

		self.setFileName(None)
		self.lastfind = None
		self.openDialog = None
		self.saveDialog = None
		self.knownEncoding = None
		self.text.focus()
		if loadFirst:
			self.update()
			self.onOpen(loadFirst, loadEncode)

	def start(self):
		self.menuBar = [
			('File', 0,
				[
				('Open...', 0, self.onOpen),
				('Save', 0, self.onSave),
				('Save As...', 5, self.onSaveAs),
				('New', 0, self.onNew),
				'separator',
				('Quit...', 0, self.onQuit)
				]),
			('Edit', 0,
				[
				('Undo', 0, self.onUndo),
				('Redo', 0, self.onRedo),
				'separator',
				('Cut', 0, self.onCut),
				('Copy', 1, self.onCopy),
				('Paste', 0, self.onPaste),
				'separator',
				('Delete', 0, self.onDelete),
				('Select All', 0, self.onSelectAll)
				]),
			('Search', 0,
				[
				('Goto...', 0, self.onGoto),
				('Find...', 0, self.onFind),
				('Refind', 0, self.onRefind),
				('Change...', 0, self.onChange),
				('Grep...', 3, self.onGrep),
				]),
			('Tools', 0,
				[
				('Pick Font...', 6, self.onPickFont),
				('Font List', 0, self.onFontList),
				'separator',
				('Pick Bg...', 3, self.onPickBg),
				('Pick Fg...', 0, self.onPickFg),
				('Color List', 0, self.onColorList),
				'separator',
				('Info...', 3, self.onInfo),
				('Clone', 0, self.onClone),
				('Run Code', 0, self.onRunCode),
				])
		]

		self.toolBar = [
			('Save', self.onSave, {'side': LEFT}),
			('Cut', self.onCut, {'side': LEFT}),
			('Copy', self.onCopy, {'side': LEFT}),
			('Paste', self.onPaste, {'side': LEFT}),
			('Find', self.onRefind, {'side': LEFT}),
			('Help', self.help, {'side': RIGHT}),
			('Quit', self.onQuit, {'side': RIGHT})
		]

	def makeWidgets(self):
		name = Label(self, bg='black', fg='white')
		name.pack(side=TOP, fill=X)

		vbar = Scrollbar(self)
		hbar = Scrollbar(self, orient='horizontal')
		text = Text(self, padx=5, wrap='none')
		text.config(undo=1, autoseparators=1)

		vbar.pack(side=RIGHT, fill=Y)
		hbar.pack(side=BOTTOM, fill=X)
		text.pack(side=TOP, fill=BOTH, expand=YES)

		text.config(yscrollcommand=vbar.set)
		text.config(xscrollcommand=hbar.set)

		vbar.config(command=text.yview)
		hbar.config(command=text.xview)

		startfont = configs.get('font', self.fonts[0])
		startbg = configs.get('bg', self.colors[0]['bg'])
		startfg = configs.get('fg', self.colors[0]['fg'])
		text.config(font=startfont, bg=startbg, fg=startfg)
		if 'height' in configs:
			text.config(height=configs['height'])
		if 'width' in configs:
			text.config(width=configs['width'])
		self.text = text
		self.filelabel = name

	def my_askopenfilename(self):
		if not self.openDialog:
			self.openDialog = Open(initialdir=self.startfiledir,
									filetypes=self.ftypes
									)
		return self.openDialog.show()

	def my_asksaveasfilename(self):
		if not self.saveDialog:
			self.saveDialog = SaveAs(initialdir=self.startfiledir,
									filetypes=self.ftypes
									)
		return self.saveDialog.show()

	def onOpen(self, loadFirst='', loadEncode=''):
		if self.text_edit_modified():
			if not askyesno('PyEdit', 'Text has changed: discard changes?'):
				return

			file = loadFirst or self.my_askopenfilename()
			if not file:
				return

			if not os.path.isfile(file):
				showerror('PyEdit', 'Could not open file '+file)
				return 

			text = None
			if loadEncode:
				try:
					text = open(file, 'r', encoding=loadEncode).read()
					self.knownEncoding = loadEncode
				except (UnicodeError, LookupError, IOError):
					pass

			if text==None and self.opensAskUser:
				self.update()
				askuser = askstring('PyEdit', 'Enter Unicode encoding for open',
									initialvalue=(self.opnesEncoding or sys.getdefaultencoding() or '')
					)

				if askuser:
					try:
						text = open(file, 'r', encoding=askuser).read()
					except (UnicodeError, LookupError, IOError):
						pass

			if text==None and self.opnesEncoding:
				try:
					text = open(file, 'r', encoding=self.opnesEncoding).read()
					self.knownEncoding = self.opnesEncoding
				except (UnicodeError, LookupError, IOError):
					pass

			if text==None:
				try:
					text = open(file, 'r', encoding=self.getdefaultencoding()).read()
					self.knownEncoding = sys.getdefaultencoding()
				except (UnicodeError, LookupError, IOError):
					pass

			if text==None:
				try:
					text = open(file, 'rb').read()
					text = text.replace(b'\r\n', b'\n')
					self.knownEncoding = None
				except IOError:
					pass

				if text==None:
					showerror('PyEdit', 'Could not decode and open file '+file)
				else:
					self.setAllText(text)
					self.setFileName(file)
					self.text.edit_reset()
					self.text.edit_modified(0)

	def onSave(self):
		self.onSaveAs(self.currfile)

	def onSaveAs(self, forcefile=None):
		filename = forcefile or self.my_asksaveasfilename()
		if not filename:
			return

		text = self.getAllText()
		encpick = None

		if self.knownEncoding and (
			(forcefile and self.savesUseKnownEncoding >= 1) or
			(not forcefile and self.savesUseKnownEncoding >= 2)):
			try:
				text.encode(self.knownEncoding)
				encpick = self.knownEncoding
			except UnicodeError:	
				pass

			if not encpick and self.savesAskUser:
				self.update()
				askuser = askstring('PyEdit', 'Enter Unicode encoding for save',
									initialvalue=(self.knownEncoding or 
												  self.savesEncoding or
												  sys.getdefaultencoding() or '')
									)
				if askuser:
					try:
						text.encode(askuser)
						encpick = askuser
					except (UnicodeError, LookupError):
						pass

				if not encpick and self.savesEncoding:
					try:
						text.encode(self.savesEncoding)
						encpick = self.savesEncoding
					except (UnicodeError, LookupError):
						pass

				if not encpick:
					try:
						text.encode(sys.getdefaultencoding())
						encpick = sys.getdefaultencoding()
					except (UnicodeError, LookupError):
						pass

				if not encpick:
					showerror('PyEdit', 'Could not encode for file'+filename)
				else:
					try:
						file = open(filename, 'w', encoding=encpick)
						file.write(text)
						file.close()
					except:
						showerror('PyEdit', 'Could not encode for file'+filename)
					else:
						self.setFileName(filename)
						self.text.edit_modified(0)
						self.knownEncoding = encpick

	def onNew(self):
		if self.text_edit_modified():
			if not askyesno('PyEdit', 'Text has changed: discard changes?'):
				return self.setFileName(None)

		self.clearAllText()
		self.text.edit_reset()
		self.text.edit_modified(0)
		self.knownEncoding = None

	def onQuit(self):
		assert False, 'onQuit must be defined in window-specific subclass'

	def text_edit_modified(self):
		return self.text_edit_modified()

	def onUndo(self):
		try:
			self.text.edit_undo()
		except TclError:
			showinfo('PyEdit', 'Nothing to undo')

	def onRedo(self):
		try:
			self.text.edit_redo()
		except TclError:
			showinfo('PyEdit', 'Nothing to redo')

	def onCopy(self):
		if not self.text.tag_range(SEL):
			showinfo('PyEdit', 'No text selected')
		else:
			text = self.text.get(SEL_FIRST, SEL_LAST)
			self.clipboard_clear()
			self.clipboard_append(txt)

	def onDelete(self):
		if not self.text.tag_range(SEL):
			showinfo('PyEdit', 'No text selected')
		else:
			self.text.delete(SEL_FIRST, SEL_LAST)

	def onCut(self):
		if not self.text.tag_range(SEL):
			showinfo('PyEdit', 'No text selected')
		else:
			self.onCopy()
			self.onDelete()

	def onPaste(self):
		try:
			text = self.selection_get(selection='CLIPBOARD')
		except TclError:
			showinfo('PyEdit', 'Nothing to paste')
			return
		self.text.insert(INSERT, text)
		self.text.tag_remove(SEL, '1.0', END)
		self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
		self.text.see(INSERT)

	def onGoto(SEL, forceline=None):
		line = forceline or askinteger('PyEdit', 'Enter line number')
		self.text.update()
		self.text.focus()
		if line is not None:
			maxindex = self.text.index(END+'-1c')
			maxline = int(maxindex.split('.')[0])
			if line > 0 and line <= maxline:
				self.text.mark_set(INSERT, '%d.0' % line)
				self.text.tag_remove(SEL, '1.0', END)
				self.text.tag_add(SEL, INSERT,'insert +1l')
				self.text.see(INSERT)
			else:
				showerror('PyEdit', 'Bad line number')

	def onFind(self, lastkey=None):
		key = lastkey or askstring('PyEdit', 'Enter search string')
		self.text.update()
		self.text.focus()
		self.lastfind = key
		if key:
			nocase = configs.get('caseinsens', True)
			where = self.text.search(key, INSERT, END, nocase=nocase)
			if no where:
				showerror('PyEdit', 'String not found')
			else:
				pastkey = where + '+%dc' % len(key)
				self.text.tag_remove(SEL, '1.0', END)
				self.text.tag_add(SEL, where, pastkey)
				self.text.mark_set(INSERT, pastkey)
				self.text.see(where)

	def onRefind(self):
		self.onFind(self.lastfind)

	def onChange(self):
		new = Toplevel(self)
		new.title('PyEdit -change')
		Label(new, text='Find text?', relief=RIDGE, width=15).grid(row=0, column=0)
		Label(new, text='Change to?', relief=RIDGE, width=15).grid(row=1, column=0)
		entry1 = Entry(new)
		entry2 = Entry(new)
		entry1.grid(row=0, column=1, sticky=EW)
		entry2.grid(row=1, column=1, sticky=EW)

		def onFind():
			self.onFind(entry1.get())

		def onApply():
			self.onDoChange(entry1.get(), entry2.get())

		Button(new, text='Find', command=onFind).grid(row=0, column=2, sticky=EW)
		Button(new, text='Apply', command=onApply).grid(row=1, column=2, sticky=EW)
		new.columnconfigure(1,weight=1)

	def onDoChange(self, findtext, changeto):
		if self.text.tag_range(SEL):
			self.text.delete(SEL_FIRST, SEL_LAST)
			self.text.insert(INSERT, changeto)
			self.text.see(INSERT)
			self.onFind(findtext)
			self.text.update()

	def onGrep(self):
		from formrows import makeFormRow
		popup = Toplevel()
		popup.title('PyEdit - grep')
		var1 = makeFormRow(popup, label='Directory root',	width=18, browse=False)
		var2 = makeFormRow(popup, label='Filename pattern', width=18, browse=False)
		var3 = makeFormRow(popup, label='Search string',  	width=18, browse=False)
		var4 = makeFormRow(popup, label='Content encoding', width=18, browse=False)

		var1.set('.')
		var2.set('*.py')
		var4.set(sys.getdefaultencoding())
		cb = lambda: self.onDoGrep(var1.get(),var2.get(),var3.get(),var4.get())
		Button(popup, text='Go', command=cb).pack()

	def onDoGrep(self, dirname, filenamepatt, grepkey, encoding):
		import threading, queue

		mypopup = Tk()
		mypopup.title('PyEdit - grepping')
		status = Label(mypopup, text='Grep thread searching for: %r...' % grepkey)
		status.pack(padx=20, pady=20)
		mypopup.protocol('WM_DELETE_WINDOW', lambda:None)

		myqueue = queue.Queue()
		threadargs = (filenamepatt, dirname, grepkey, encoding, myqueue)
		threading.Thread(target=self.grepThreadProducer, args=threadargs).start()
		self.grepThreadConsumer(grepkey, encoding, myqueue, mypopup)

	def grepThreadProducer(self, filenamepatt, dirname, grepkey, encoding, myqueue):
		pass

