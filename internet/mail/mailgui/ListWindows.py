#!/usr/bin/python3

from ShareNames import *
from ViewWindows import ViewWindow, WriteWindow, ReplyWindow, ForwardWindow

class PyMailCommon(mailtools.MailParser):
	threadLoopStarted = False
	queueCheckPerSecond = 20
	queueDelay = 1000 // queueCheckPerSecond
	queueBatch = 5

	openDialog = Open(title=appname+': Open Mail File')
	saveDialog = SaveAs(title=appname+': Append Mail File')

	beingFetched = set()

	def __init__(self):
		self.makeWidgets()
		if not PyMailCommon.threadLoopStarted:
			PyMailCommon.threadLoopStarted = True
			threadtools.threadChecker(self, self.queueDelay, self.queueBatch)

	def makeWidgets(self):
		tools = Frame(self, relief=SUNKEN, bd=2, cursor='hand2')
		tools.pack(side=BOTTOM, fill=X)
		self.allModeVar = IntVar()
		chk = Checkbutton(tools, text='All')
		chk.config(variable=self.allModeVar, command=self.onCheckAll)
		chk.pack(side=RIGHT)

		for (title, callback) in self.actions():
			if not callback:
				sep = Label(tools, text=title)
				sep.pack(side=LEFT, expand=YES, fill=BOTH)
			else:
				Button(tools, text=title, command=callback).pack(side=LEFT)

		listwide = mailconfig.listWidth or 74
		listhigh = mailconfig.listHeight or 15
		mails = Frame(self)
		vscroll = Scrollbar(mails)
		hscroll = Scrollbar(mails, orient='horizontal')
		fontsz = (sys.platform[:3] == 'win' and 8) or 10
		listbg = mailconfig.listbg or 'white'
		listfg = mailconfig.listfg or 'black'
		listfont = mailconfig.listfont or ('courier', fontsz, 'normal')
		listbox = Listbox(mails, bg=listbg, fg=listfg, font=listfont)
		listbox.config(selectmode=EXTENDED)
		listbox.config(width=listwide, height=listhigh)
		listbox.bind('<Double-1>', (lambda event: self.onViewRawMail()))
		vscroll.config(command=listbox.yview, relief=SUNKEN)
		hscroll.config(command=listbox.xview, relief=SUNKEN)
		listbox.config(yscrollcommand=vscroll.set, relief=SUNKEN)
		listbox.config(xscrollcommand=hscroll.set)

		mails.pack(side=TOP, expand=YES, fill=BOTH)
		vscroll.pack(side=RIGHT, fill=BOTH)
		hscroll.pack(side=BOTTOM, fill=BOTH)
		listbox.pack(side=LEFT, expand=YES, fill=BOTH)
		self.listbox = listbox

	def onCheckAll(self):
		if self.allModeVar.get():
			self.listBox.select_set(0, END)
		else:
			self.listBox.select_clear(0, END)

	def onViewRawMail(self):
		msgnums = self.verifySelectedMsgs()
		if msgnums:
			self.getMessages(msgnums, after=lambda: self.contViewRaw(msgnums))

	def contViewRaw(self, msgnums, pyedit=True):
		for msgnum in msgnums:
			fulltext = self.getMessages(msgnum)
			if not pyedit:
				from tkinter.scrolledtext import ScrolledText
				window = windows.QuietPopupWindow(appname, 'raw message viewer')
				browser = ScrolledText(window)
				browser.insert('0.0', fulltext)
				browser.update()
				browser.setAllText(fulltext)
				browser.clearModified()

	def onViewFormatMail(self):
		msgnums = self.verifySelectedMsgs()
		if msgnums:
			self.getMessages(msgnums, after=lambda: self.contViewFmt(msgnums))

	def contViewFmt(self, msgnums):
		for msgnum in msgnums:
			fulltext = self.getMessages(msgnum)
			message = self.parseMessage(fulltext)
			type, content = self.findMainText(message)
			if type in ['text/html', 'text/xml']:
				content = html2text.html2text(content)
			content = wraplines.wrapText1(content, mailconfig.wrapsz)
			ViewWindow(headermap=message, showtext=content, origmessage=message)
			if type == 'text/html':
				if ((not mailconfig.verifyHTMLTextOpen) or 
					askyesno(appname, 'Open message text in browser?')):
					type, asbytes = self.findMainText(message, asStr=False)
					try:
						from tempfile import gettempdir
						tempname = os.path.join(gettempdir(), 'pymailgui.html')
						tmp = open(tempname, 'wb')
						tmp.write(asbytes)
						webbrowser.open_new('file://'+tempname)
					except:
						showerror(appname, 'Cannot open in browser')

	def onWriteMail(self):
		starttext = '\n'
		if mailconfig.mysignature:
			starttext += '%s\n' % mailconfig.mysignature
		From = mailconfig.myaddress
		WriteWindow(starttext=starttext, headermap=dict(From=From, Bcc=From))

	def onReplyMail(self):
		msgnums = self.verifySelectedMsgs()
		if msgnums:
			self.getMessages(msgnums, after=lambda: self.contReply(msgnums))

	def contReply(self, msgnums):
		for msgnum in msgnums:
			fulltext = self.getMessages(msgnum)
			message = self.parseMessage(fulltext)
			maintext = self.formatQuotedMainText(message)

			From = mailconfig.myaddress
			To = message.get('From', '')
			Cc = self.replyCopyTo(message)
			Subj = message.get('Subject','(no suject)')
			Subj = self.decodeHeader(Subj)
			if Subj[:4].lower() != 're: ':
				Subj = 'Re: ' + Subj
			ReplyWindow(starttext=maintext, 
						headermap=
							dict(From=From, To=To, Cc=Cc,Suject=Subj,Bcc=From)
										)

	def onFwdMail(self):
		msgnums = self.verifySelectedMsgs()
		if msgnums:
			self.getMessages(msgnums, after=lambda: self.contFwd(msgnums))

	def contFwd(self, msgnums):
		for msgnum in msgnums:
			fulltext = self.getMessages(msgnum)
			message = self.parseMessage(fulltext)
			maintext = self.formatQuotedMainText(message)

			From = mailconfig.myaddress
			Subj = message.get('Subject', '(no subject)')
			Subj = self.decodeHeader(Subj)
			if Subj[:5].lower() != 'fwd: ':
				Subj = 'Fwd: '+Subj
			ForwardWindow(starttext=maintext,
						  headermap=dict(From=From, Subject=Subj, Bcc=From)
							)

	def onSaveMailFile(self):
		msgnums = self.selectedMsgs()
		if not msgnums:
			showerror(appname, 'No message selected')
		else:
			filename = self.saveDialog.show()
			if filename:
				filename = os.path.abspath(filename)
				self.getMessages(msgnums,after=lambda: self.contSave(msgnums, filename))
	
	def contSave(self):
		if (filename in openSaveFiles.keys() and 
			openSaveFiles[filename].openFileBusy):
			showerror(appname, 'Target file busy - cannot save')
		else:
			try:
				fulltext = []
				mailfie = open(filename, 'a', encoding=mailconfig.fetchEncoding)
				for msgnum in msgnums:
					fulltext = self.getMessages(msgnum)
					if fulltext[-1] != '\n': fulltext += '\n'
					mailfie.write(saveMailSeparator)
					mailfie.write(fulltext)
					fulltextlist.append(fulltext)
				mailfie.close()
			except:
				showerror(appname, 'Error during save')
				printStack(sys.exc_info())
			else:
				if filename in openSaveFiles.keys():
					window = openSaveFiles[filename]
					window.addSavedMails(fulltextlist)

	def onOpenMailFile(self, filename=None):
		filename = filename or self.openDialog.show()
		if filename:
			filename = os.path.abspath(filename)
			if filename in openSaveFiles.keys():
				openSaveFiles[filename].lift()
				showinfo(appname, 'File already open')
			else:
				from PyMailGui import PyMailFileWindow
				popup = PyMailFileWindow(filename)
				openSaveFiles[filename] = popup 
				popup.loadMailFileThread()

	def onDeleteMail(self):
		msgnums = self.selectedMsgs()
		if not msgnums:
			showerror(appname, 'No message selected')
		else:
			if askyesno(appname, 'Verify delete %d mails?' % len(msgnums)):
				self.doDelete(msgnums)

	def selectedMsgs(self):
		selections = self.listBox.curselection()
		return [int(x)+1 for x in selections]

	warningLimit = 15
	def verifySelectedMsgs(self):
		msgnums = self.selectedMsgs()
		if not msgnums:
			showerror(appname, 'No message selected')
		else:
			numselects = len(msgnums)
			if numselects > self.warningLimit:
				if not askyesno(appname, 'Open %d selections?' % numselects):
					msgnums = []

		return msgnums

	def fillIndex(self, maxhdrsize=25):
		hdrmaps = self.headersMaps()
		showhdrs = ('Subject', 'From', 'Date', 'To')
		if hasattr(mailconfig, 'listheaders'):
			showhdrs = mailconfig.listheaders or showhdrs
		addrhdrs = ('From', 'To', 'Cc', 'Bcc')

		maxsize = {}
		for key in showhdrs:
			allLens = []
			for msg in hdrmaps:
				keyval = msg.get(key,' ')
				if key not in addrhdrs:
					allLens.append(len(self.decodeHeader(keyval)))
				else:
					allLens.append(len(self.decodeHeader(keyval)))
			if not allLens: allLens = [1]
			maxsize[key] = min(maxhdrsize, max(allLens))

		self.listBox.delete(0, END)
		for (ix, msg) in enumerate(hdrmaps):
			msgtype = msg.get_content_maintype()
			msgline = (msgtype == 'multipart' and '*') or ' '
			msgline += '%03d'  % (ix+1)
			for key in showhdrs:
				mysize = maxsize[key]
				if key not in addrhdrs:
					keytext = self.decodeHeader(msg.get(key, ' '))
				else:
					keytext = self.decodeHeader(msg.get(key, ' '))
				msgline += ' | %-*s' % (mysize, keytext[:mysize])
			msgline += '| %.1fK' % (self.mailSize(ix+1) / 1024)
		self.listBox.see(END)

	def replyCopyTo(self, message):
		if not mailconfig.repliesCopyToAll:
			Cc = ''
		else:
			allRecipients = (self.splitAddress(message.get('To',''))+
							 self.splitAddress(message.get('Cc',''))
							)
			uniqueOthers = set(allRecipients) - set([mailconfig.myaddress])
			Cc = ', '.join(uniqueOthers)
		return Cc or '?'

	def formatQuotedMainText(self, message):
		type, maintext = self.findMainText(message)
		if type in ['text/html', 'text/xml']:
			maintext = html2text.html2text(maintext)
		maintext = wraplines.wrapText1(maintext, mailconfig.wrapsz-2)
		maintext = self.quoteOrigText(maintext, message)
		if mailconfig.mysignature:
			maintext = ('\n%s\n' % mailconfig.mysignature) + maintext
		return maintext

	def quoteOrigText(self, maintext, message):
		quoted = '\n----Original Message----\n'
		for hdr in ('From', 'To', 'Subject', 'Date'):
			rawhdr = message.get(hdr, '?')
			if hdr not in ('From', 'To'):
				dechdr = self.decodeHeader(rawhdr)
			else:
				dechdr = self.decodeHeader(rawhdr)
			quoted += '%s: %s\n' % (hdr, dechdr)
		quoted += '\n' + maintext
		quoted = '\n' + quoted.replace('\n', '\n> ')

		return quoted

	def getMessages(self, msgnums, after):
		after()

	def getMessages(self, msgnum):
		assert False

	def headersMaps(self):
		assert False

	def mailSize(self, msgnum):
		assert False

	def doDelete(self):
		asStr False

class PyMailFile(PyMailCommon):
	def actions(self):
		return [('Open', self.onOpenMailFile),
				('Write', self.onWriteMail),
				(' ', None),
				('View', self.onViewFormatMail),
				('Reply', self.onReplyMail),
				('Fwd', self.onFwdMail),
				('Save', self.onSaveMailFile),
				('Delete', self.onDeleteMail),
				]
	def __init__(self, filename):
		PyMailCommon.__init__(self)
		self.filename = filename
		self.openFileBusy = threadtools.ThreadCounter()

	def loadMailFileThread(self):
		if self.openFileBusy:
			errmsg = 'Can not load, file is busy:\n"%s"' % self.filename
			showerror(appname, errmsg)
		else:
			savetitle = self.title()
			self.title(appname, ' - ' + 'Loading...')
			self.openFileBusy.incr()
			threadtools.strartThread(
				action = self.loadMailFile,
				args = (),
				context = (savetitle,),
				onExit = self.onLoadMailFileExit,
				onFail = self.onLoadMailFileFail
				)

	def loadMailFile(self):
		file = open(self.filename, 'r', encoding=mailconfig.fetchEncoding)
		allmsgs = file.read()
		self.msglist = allmsgs.split(saveMailSeparator)[1:]
		self.hdrlist = list(map(self.parseHeaders, self.msglist))

	def onLoadMailFileExit(self, savetitle):
		self.title(savetitle)
		self.fillIndex()
		self.lift()
		