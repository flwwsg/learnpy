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

	def onFwdMain(self):
		msgnums = self.verifySelectedMsgs()
		if msgnums:
			self.getMessages(msgnums, after=lambda: self.contFwd(msgnums))

	def contFwd(self, msgnums):
		for msgnum in msgnums:
			fulltext 